use crate::eilendvm::object::base_object::{EObj, EObjRef};
use std::any::Any;
use std::cell::{Ref, RefCell};
use std::rc::Rc;
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

pub fn v_obj_box() -> EObjRef {
    Rc::new(RefCell::new(v_obj()))
}

pub fn as_obj(value: &Rc<RefCell<dyn EObj>>) -> Ref<'_, dyn EObj> {
    // some shitty magic i do not want to understand
    // thx lubaskinc0de for that snippet
    let v = value.borrow();
    Ref::map(v, |v| v)
}
