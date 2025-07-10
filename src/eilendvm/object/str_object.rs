use std::any::Any;
use std::ops::Deref;
use crate::eilendvm::object::base_object::{EObj, EObjDyn, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct EStr {
    table: Table,
    value: String
}

eobj_common_impl!(EStr, EObjTyp::STR);

impl EStr {
    pub fn get_value(&self) -> &String { &self.value }
}


pub fn v_str(value: String) -> EStr {
    EStr {
        table: Table::new(),
        value
    }
}

pub fn v_str_box(value: String) -> EObjDyn {
    Box::new(EStr {
        table: Table::new(),
        value
    })
}

pub fn as_estr(value: &EObjDyn) -> &EStr {
    match value.typ() {
        EObjTyp::STR =>
            value.as_any().downcast_ref::<EStr>().expect("failed to downcast EStr"),
        _ => panic!("tried to downcast {} as EStr", value.typ())
    }
}