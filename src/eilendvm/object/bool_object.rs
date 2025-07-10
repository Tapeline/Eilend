use std::any::Any;
use crate::eilendvm::object::base_object::{EObj, EObjDyn, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};

pub struct EBool {
    table: Table,
    value: bool
}

impl EObj for EBool {
    eobj_common_impl!(EObjTyp::BOOL);

    fn display_str(&self) -> String {
        self.value.to_string()
    }
}

impl EBool {
    pub fn get_value(&self) -> bool { self.value }
}

eobj_common_converters!(EBool, bool, EObjTyp::BOOL, bool);
