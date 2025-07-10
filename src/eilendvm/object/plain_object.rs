use crate::eilendvm::object::base_object::EObj;
use std::any::Any;
use crate::eilendvm::object::base_object::EObjTyp;
use crate::eilendvm::object::table::Table;
use crate::eobj_common_impl;

pub struct EObject {
    table: Table,
}

impl EObj for EObject {
    eobj_common_impl!(EObjTyp::PLAIN);
}
