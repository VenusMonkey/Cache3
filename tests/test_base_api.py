#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date: 2023/2/15

import pytest
from cache3.utils import empty
from cache3 import MiniCache, Cache, DiskCache

params = pytest.mark.parametrize
raises = pytest.raises

key_types_cases = [
    # string
    ('key', 'value'),

    # float
    (3.3, 'float1'),
    (.3, 'float2'),
    (3., 'float'),

    # integer
    (3, 'integer'),

    # empty
    (empty, 'empty'),

    # bool
    (True, 'bool-true'),
    (1, 'bool-true-mess-1'),
    ('true', 'bool-true-mess-2'),
    (False, 'bool-false'),
    (0, 'bool-false-mess-1'),
    ('false', 'bool-false-mess-2'),
]

class TestGeneralCacheApi:

    def setup_class(self):
        self.caches = [
            Cache('memory_cache'),
            DiskCache('disk_cache'),
        ]

    def setup_method(self):
        assert all((cache.clear() for cache in self.caches))

    @params('key, value', key_types_cases)
    def test_set_get(self, key, value):
        for cache in self.caches:
            cache.set(key, value)
            assert cache.pop(key) == value
            cache.set(value, key)
            assert cache.pop(value) == key

    def test_set_get_tag(self):
        for cache in self.caches:
            cache.set('name', 'value', tag='1')
            assert cache.get('name', empty) == empty
            assert cache.get('name', tag='1') == 'value'

    def test_clear(self):
        for cache in self.caches:
            cache.clear()
            cache.set('k', 'v')
            assert len(cache) == 1
            assert cache.clear()
            assert len(cache) == 0

    def test_ex_set(self):
        for cache in self.caches:
            assert cache.ex_set('name', None)
            assert not cache.ex_set('name', None)

    def test_incr_decr(self):
        count = 'count'
        for cache in self.caches:
            assert cache.set(count, 0)
            assert cache.incr(count, 1) == 1
            assert cache.decr(count, 1) == 0
            
            with raises(KeyError, match='key .* not found in cache'):
                cache.incr('no-existed')
            
            cache.set('not-number', 'a')
            with raises(TypeError, match='unsupported operand type'):
                cache.incr('not-number') 

    @params('key, value, tag', [
        ('name', 'value', None),
        (empty, 'empty', None),
        (1111, 1111, None),
        (1111, 1111, 'tag-1'),
        ('empty', empty, 'tag-1'),
        ('empty', 'empty', 'tag-2'),
    ])
    def test_has_key(self, key, value, tag):
        for cache in self.caches:
            cache.set(key, value, tag=tag)
            assert cache.has_key(key, tag=tag)
            cache.delete(key, tag=tag)
            assert not cache.has_key(key, tag=tag)
    

