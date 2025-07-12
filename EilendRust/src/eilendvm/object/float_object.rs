use crate::eilendvm::object::base_object::EObjRef;
use std::cell::Ref;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};

pub struct EFloat {
    table: Table,
    value: f64
}

impl EObj for EFloat {
    eobj_common_impl!(EObjTyp::FLOAT);

    fn display_str(&self) -> String {
        self.value.to_string()
    }
}

impl EFloat {
    pub fn get_value(&self) -> f64 { self.value }
}

eobj_common_converters!(EFloat, float, EObjTyp::FLOAT, f64);
