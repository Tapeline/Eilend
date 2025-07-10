use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjDyn, EObjTyp};
use crate::eilendvm::object::str_object::EStr;
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct EInt {
    table: Table,
    value: i64
}

eobj_common_impl!(EInt, EObjTyp::INT);

impl EInt {
    pub fn get_value(&self) -> i64 { self.value }
}


pub fn v_int(value: i64) -> EInt {
    EInt {
        table: Table::new(),
        value
    }
}

pub fn v_int_box(value: i64) -> EObjDyn {
    Box::new(EInt {
        table: Table::new(),
        value
    })
}

pub fn as_eint(value: &EObjDyn) -> &EInt {
    match value.typ() {
        EObjTyp::INT =>
            value.as_any().downcast_ref::<EInt>().expect("failed to downcast EInt"),
        _ => panic!("tried to downcast {} as EInt", value.typ())
    }
}
