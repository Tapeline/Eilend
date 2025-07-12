use std::any::Any;
use std::cell::RefCell;
use std::fmt::Display;
use std::rc::Rc;
use crate::eilendvm::object::table::Table;

pub enum EObjTyp {
    PLAIN, INT, FLOAT, STR, BOOL, NULL, FUNC
}

impl Display for EObjTyp {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            EObjTyp::PLAIN => write!(f, "PLAIN"),
            EObjTyp::INT => write!(f, "INT"),
            EObjTyp::FLOAT => write!(f, "FLOAT"),
            EObjTyp::STR => write!(f, "STR"),
            EObjTyp::BOOL => write!(f, "BOOL"),
            EObjTyp::NULL => write!(f, "NULL"),
            EObjTyp::FUNC => write!(f, "FUNC"),
        }
    }
}

pub type EObjRef = Rc<RefCell<dyn EObj>>;

pub trait EObj {

    // Utility ops
    fn get_table(&self) -> &Table;
    fn get_table_mut(&mut self) -> &mut Table;
    fn typ(&self) -> &EObjTyp;
    fn as_any(&self) -> &dyn Any;
    fn as_any_mut(&mut self) -> &mut dyn Any;

    // Common object operations
    fn display_str(&self) -> String {
        "Obj".to_string()
    }

    fn is_truthy(&self) -> bool { true }
    fn is_falsy(&self) -> bool { false }
}
