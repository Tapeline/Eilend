use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;
use crate::eilendvm::object::base_object::{EObj, EObjRef};

pub struct Table {
    map: HashMap<String, EObjRef>,
    uptable: Option<Rc<RefCell<Table>>>,
}

impl Table {
    pub fn new() -> Table {
        Table{map: HashMap::new(), uptable: None}
    }

    pub fn set_uptable(&mut self, uptable: Rc<RefCell<Table>>) -> &mut Table {
        self.uptable = Some(uptable);
        self
    }

    pub fn get(&self, key: &str) -> Option<EObjRef> {
        if let Some(value) = self.map.get(key) {
            return Some(value.clone())
        }
        if let Some(uptable) = &self.uptable {
            if let Some(value) = uptable.borrow().get(key) {
                return Some(value.clone())
            }
        }
        None
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
