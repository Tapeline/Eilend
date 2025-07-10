use std::collections::HashMap;
use crate::eilendvm::object::base_object::{EObj, EObjDyn};

pub struct Table {
    map: HashMap<String, EObjDyn>
}

impl Table {
    pub fn new() -> Table {
        Table{map: HashMap::new()}
    }

    pub fn get(&self, key: &str) -> Option<&EObjDyn> {
        self.map.get(key)
    }

    pub fn put(&mut self, key: String, obj: EObjDyn) {
        self.map.insert(key, obj);
    }

    pub fn remove(&mut self, key: &str) {
        self.map.remove(key);
    }

    pub fn len(&self) -> usize {
        self.map.len()
    }
}