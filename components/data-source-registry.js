/**
 * Data Source Registry (DSR) - Browser (public beta) implementation
 * - localStorage persistence
 * - CRUD + soft delete + version snapshots
 * - simple search/filter
 * - health/status updates
 *
 * Global:
 *   window.DataSourceRegistry  (singleton instance)
 */

(function initDataSourceRegistry(global) {
  'use strict';

  const STORAGE_KEY = 'jingjie:data-sources:v1';
  const EVENT_NAME = 'jingjie:datasource:changed';

  function nowIso() {
    return new Date().toISOString();
  }

  function uuid() {
    if (global.crypto && typeof global.crypto.randomUUID === 'function') {
      return global.crypto.randomUUID();
    }
    // Fallback: not cryptographically perfect, but ok for demo/public beta.
    return 'ds_' + Math.random().toString(36).slice(2) + '_' + Date.now().toString(36);
  }

  function safeJsonParse(value, fallback) {
    try {
      return JSON.parse(value);
    } catch {
      return fallback;
    }
  }

  function normalizeTags(tags) {
    if (!tags) return [];
    if (Array.isArray(tags)) {
      return tags.map(t => String(t).trim()).filter(Boolean);
    }
    if (typeof tags === 'string') {
      return tags
        .split(',')
        .map(t => t.trim())
        .filter(Boolean);
    }
    return [];
  }

  function normalizeString(v) {
    return (v == null ? '' : String(v)).trim();
  }

  function toLower(v) {
    return normalizeString(v).toLowerCase();
  }

  function validateCreate(input) {
    const name = normalizeString(input.name);
    const type = normalizeString(input.type);
    const endpoint = normalizeString(input.endpoint);

    if (!name) throw new Error('資料源名稱不可為空');
    if (!type) throw new Error('資料源類型不可為空');
    if (!endpoint) throw new Error('資料源端點/URL 不可為空');
  }

  class DataSourceRegistry {
    constructor() {
      this._cache = null;
      this._load();
    }

    _emit(detail) {
      try {
        global.dispatchEvent(new CustomEvent(EVENT_NAME, { detail }));
      } catch {
        // ignore
      }
    }

    _load() {
      const raw = global.localStorage ? global.localStorage.getItem(STORAGE_KEY) : null;
      const data = safeJsonParse(raw || '', null);
      if (data && typeof data === 'object' && Array.isArray(data.items)) {
        this._cache = data;
        return;
      }
      this._cache = { schema: 1, items: [] };
      this._save();
    }

    _save() {
      if (!global.localStorage) return;
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(this._cache));
    }

    _items() {
      if (!this._cache) this._load();
      return this._cache.items;
    }

    seedIfEmpty(seedItems) {
      const items = this._items();
      if (items.length > 0) return { seeded: false, count: items.length };

      const now = nowIso();
      const created = (seedItems || []).map(s => {
        const record = {
          id: uuid(),
          name: normalizeString(s.name),
          description: normalizeString(s.description),
          type: normalizeString(s.type || 'api'),
          endpoint: normalizeString(s.endpoint || ''),
          region: normalizeString(s.region || '全球'),
          tags: normalizeTags(s.tags),
          categoryPath: Array.isArray(s.categoryPath) ? s.categoryPath.map(normalizeString).filter(Boolean) : [],
          status: normalizeString(s.status || 'healthy'), // healthy | degraded | down
          health: {
            uptime: typeof s.uptime === 'number' ? s.uptime : null,
            responseTimeMs: typeof s.responseTimeMs === 'number' ? s.responseTimeMs : null,
            lastCheckAt: s.lastCheckAt || null
          },
          version: 1,
          versions: [],
          deletedAt: null,
          createdAt: now,
          updatedAt: now
        };
        validateCreate(record);
        return record;
      });

      this._cache.items = created;
      this._save();
      this._emit({ type: 'seed', count: created.length });
      return { seeded: true, count: created.length };
    }

    list(options = {}) {
      const {
        includeDeleted = false,
        query = '',
        status = null,
        type = null,
        tag = null
      } = options;

      const q = toLower(query);
      const items = this._items().filter(ds => {
        if (!includeDeleted && ds.deletedAt) return false;
        if (status && normalizeString(ds.status) !== normalizeString(status)) return false;
        if (type && normalizeString(ds.type) !== normalizeString(type)) return false;
        if (tag && !Array.isArray(ds.tags)) return false;
        if (tag && !ds.tags.map(toLower).includes(toLower(tag))) return false;
        if (!q) return true;

        const hay = [
          ds.name,
          ds.description,
          ds.type,
          ds.endpoint,
          Array.isArray(ds.tags) ? ds.tags.join(' ') : ''
        ]
          .map(toLower)
          .join(' | ');

        return hay.includes(q);
      });

      // newest first
      return items.slice().sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
    }

    get(id) {
      const item = this._items().find(ds => ds.id === id);
      return item ? JSON.parse(JSON.stringify(item)) : null;
    }

    create(input, meta = {}) {
      validateCreate(input);
      const now = nowIso();
      const record = {
        id: uuid(),
        name: normalizeString(input.name),
        description: normalizeString(input.description),
        type: normalizeString(input.type),
        endpoint: normalizeString(input.endpoint),
        region: normalizeString(input.region || '全球'),
        tags: normalizeTags(input.tags),
        categoryPath: Array.isArray(input.categoryPath) ? input.categoryPath.map(normalizeString).filter(Boolean) : [],
        status: normalizeString(input.status || 'healthy'),
        health: {
          uptime: typeof input.uptime === 'number' ? input.uptime : null,
          responseTimeMs: typeof input.responseTimeMs === 'number' ? input.responseTimeMs : null,
          lastCheckAt: input.lastCheckAt || null
        },
        version: 1,
        versions: [],
        deletedAt: null,
        createdAt: now,
        updatedAt: now,
        createdBy: meta.actor || null
      };

      this._items().push(record);
      this._save();
      this._emit({ type: 'create', id: record.id });
      return this.get(record.id);
    }

    update(id, patch, meta = {}) {
      const items = this._items();
      const idx = items.findIndex(ds => ds.id === id);
      if (idx === -1) throw new Error('找不到資料源');

      const current = items[idx];
      if (current.deletedAt) throw new Error('資料源已刪除（軟刪除），請先還原');

      const snapshot = JSON.parse(JSON.stringify(current));
      const next = { ...current };

      if (patch.name != null) next.name = normalizeString(patch.name);
      if (patch.description != null) next.description = normalizeString(patch.description);
      if (patch.type != null) next.type = normalizeString(patch.type);
      if (patch.endpoint != null) next.endpoint = normalizeString(patch.endpoint);
      if (patch.region != null) next.region = normalizeString(patch.region);
      if (patch.tags != null) next.tags = normalizeTags(patch.tags);
      if (patch.categoryPath != null) next.categoryPath = Array.isArray(patch.categoryPath) ? patch.categoryPath.map(normalizeString).filter(Boolean) : [];
      if (patch.status != null) next.status = normalizeString(patch.status);
      if (patch.health != null && typeof patch.health === 'object') {
        next.health = { ...(next.health || {}), ...patch.health };
      }

      validateCreate(next);

      // Versioning
      const createVersion = meta.createVersion !== false;
      if (createVersion) {
        const v = {
          version: current.version,
          at: nowIso(),
          by: meta.actor || null,
          data: snapshot
        };
        next.versions = Array.isArray(current.versions) ? current.versions.slice() : [];
        next.versions.unshift(v);
        next.version = (current.version || 1) + 1;
      }

      next.updatedAt = nowIso();
      next.updatedBy = meta.actor || null;

      items[idx] = next;
      this._save();
      this._emit({ type: 'update', id });
      return this.get(id);
    }

    softDelete(id, meta = {}) {
      const items = this._items();
      const idx = items.findIndex(ds => ds.id === id);
      if (idx === -1) throw new Error('找不到資料源');

      const ds = { ...items[idx] };
      if (ds.deletedAt) return this.get(id);

      ds.deletedAt = nowIso();
      ds.updatedAt = ds.deletedAt;
      ds.updatedBy = meta.actor || null;
      items[idx] = ds;
      this._save();
      this._emit({ type: 'delete', id });
      return this.get(id);
    }

    restore(id, meta = {}) {
      const items = this._items();
      const idx = items.findIndex(ds => ds.id === id);
      if (idx === -1) throw new Error('找不到資料源');

      const ds = { ...items[idx] };
      if (!ds.deletedAt) return this.get(id);

      ds.deletedAt = null;
      ds.updatedAt = nowIso();
      ds.updatedBy = meta.actor || null;
      items[idx] = ds;
      this._save();
      this._emit({ type: 'restore', id });
      return this.get(id);
    }

    upsertHealth(id, healthPatch = {}) {
      const items = this._items();
      const idx = items.findIndex(ds => ds.id === id);
      if (idx === -1) throw new Error('找不到資料源');

      const ds = { ...items[idx] };
      if (ds.deletedAt) throw new Error('資料源已刪除（軟刪除），不可更新健康狀態');

      ds.health = { ...(ds.health || {}) };
      if (healthPatch.uptime != null) ds.health.uptime = healthPatch.uptime;
      if (healthPatch.responseTimeMs != null) ds.health.responseTimeMs = healthPatch.responseTimeMs;
      if (healthPatch.lastCheckAt != null) ds.health.lastCheckAt = healthPatch.lastCheckAt;

      // derive status if provided
      if (healthPatch.status) {
        ds.status = normalizeString(healthPatch.status);
      }

      ds.updatedAt = nowIso();
      items[idx] = ds;
      this._save();
      this._emit({ type: 'health', id });
      return this.get(id);
    }

    clearAll() {
      this._cache = { schema: 1, items: [] };
      this._save();
      this._emit({ type: 'clear' });
    }
  }

  // Singleton
  global.DataSourceRegistry = global.DataSourceRegistry || new DataSourceRegistry();
  global.DataSourceRegistry.EVENT_NAME = EVENT_NAME;
})(window);

