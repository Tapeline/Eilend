use crate::eilendvm::object::base_object::EObjRef;
use std::cell::Ref;
use std::cell::RefCell;
use std::rc::Rc;
use std::any::Any;
use std::fmt::format;
use crate::eilendvm::object::base_object::{EObj, EObjTyp};
use crate::eilendvm::object::table::Table;
use crate::{eobj_common_converters, eobj_common_impl};
use crate::eilendvm::chunk::CodeChunk;

pub struct EFunc {
    table: Table,
    value: FuncData
}

pub struct FuncData {
    pub name: String,
    pub arg_spec: Vec<String>,
    pub code: CodeChunk
}

impl EObj for EFunc {
    eobj_common_impl!(EObjTyp::STR);

    fn display_str(&self) -> String {
        format!("<Func {}>", self.value.name)
    }
}

impl EFunc {
    pub fn get_value(&self) -> &FuncData { &self.value }
    pub fn get_value_mut(&mut self) -> &mut FuncData { &mut self.value }

}


eobj_common_converters!(EFunc, func, EObjTyp::FUNC, FuncData);
