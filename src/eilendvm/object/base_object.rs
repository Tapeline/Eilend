use std::any::Any;
use std::fmt::Display;
use crate::eilendvm::object::table::Table;

pub type EObjDyn = Box<dyn EObj>;

pub trait EObj {
    fn get_table(&self) -> &Table;
    fn get_table_mut(&mut self) -> &mut Table;
    fn typ(&self) -> &EObjTyp;
    fn as_any(&self) -> &dyn Any;
}

#[macro_export]
macro_rules! eobj_common_impl {
    ($name: ident, $typ: expr) => {
        impl EObj for $name {
            fn get_table(&self) -> &Table {
                &self.table
            }

            fn get_table_mut(&mut self) -> &mut Table {
                &mut self.table
            }

            fn typ(&self) -> &EObjTyp {
                &$typ
            }

            fn as_any(&self) -> &dyn Any {
                self
            }
        }
    }
}

pub struct EObject {
    table: Table,
}

pub enum EObjTyp {
    PLAIN, INT, FLOAT, STR
}

impl Display for EObjTyp {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            EObjTyp::PLAIN => write!(f, "PLAIN"),
            EObjTyp::INT => write!(f, "INT"),
            EObjTyp::FLOAT => write!(f, "FLOAT"),
            EObjTyp::STR => write!(f, "STR"),
        }
    }
}

eobj_common_impl!(EObject, EObjTyp::PLAIN);
