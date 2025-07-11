use std::collections::HashMap;
use crate::eilendvm::object::base_object::{EObj, EObjRef};

pub struct Table {
    map: HashMap<String, EObjRef>
}

impl Table {
    pub fn new() -> Table {
        Table{map: HashMap::new()}
    }

    pub fn get(&self, key: &str) -> Option<&EObjRef> {
        self.map.get(key)
    }

    pub fn put(&mut self, key: String, obj: EObjRef) {
        self.map.insert(key, obj);
    }

    pub fn remove(&mut self, key: &str) {
        self.map.remove(key);
    }

    pub fn len(&self) -> usize {
        self.map.len()
    }
}
