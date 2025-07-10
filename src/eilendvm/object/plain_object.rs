use crate::eilendvm::object::base_object::{EObj, EObjDyn};
use std::any::Any;
use crate::eilendvm::object::base_object::EObjTyp;
use crate::eilendvm::object::null_object::ENull;
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct EObject {
    table: Table,
}

impl EObj for EObject {
    eobj_common_impl!(EObjTyp::PLAIN);
}

pub fn v_obj() -> EObject {
    EObject { table: Table::new() }
}

pub fn v_obj_box() -> EObjDyn {
    Box::new(v_obj())
}
