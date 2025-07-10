use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjDyn, EObjTyp};
use crate::eilendvm::object::str_object::EStr;
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct EFloat {
    table: Table,
    value: f64
}

eobj_common_impl!(EFloat, EObjTyp::FLOAT);

impl EFloat {
    pub fn get_value(&self) -> f64 { self.value }
}


pub fn v_float(value: f64) -> EFloat {
    EFloat {
        table: Table::new(),
        value
    }
}

pub fn v_float_box(value: f64) -> EObjDyn {
    Box::new(EFloat {
        table: Table::new(),
        value
    })
}

pub fn as_efloat(value: &EObjDyn) -> &EFloat {
    match value.typ() {
        EObjTyp::FLOAT =>
            value.as_any().downcast_ref::<EFloat>().expect("failed to downcast EFloat"),
        _ => panic!("tried to downcast {} as EFloat", value.typ())
    }
}
