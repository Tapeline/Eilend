#[macro_export]
macro_rules! eobj_common_impl {
    ($typ: expr) => {
        //impl EObj for $name {
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

            fn as_any_mut(&mut self) -> &mut dyn Any {
                self
            }
        //}
    }
}

#[macro_export]
macro_rules! rc_cell {
    ($expr: expr) => {
        Rc::new(RefCell::new($expr))
    };
}

#[macro_export]
macro_rules! eobj_common_converters {
    ($name: ident, $lowercase_name: ident, $obj_type: expr, $value_t: ty) => {
        paste::item! {
            pub fn [< v_ $lowercase_name >](value: $value_t) -> $name {
                $name {
                    table: Table::new(),
                    value
                }
            }

            pub fn [< v_ $lowercase_name _ref >](value: $value_t) -> EObjRef {
                Rc::new(RefCell::new($name {
                    table: Table::new(),
                    value
                }))
            }

            pub fn [<as_e $lowercase_name >](value: &Rc<RefCell<dyn EObj>>) -> Ref<'_, $name> {
                // some shitty magic i do not want to understand
                // thx lubaskinc0de for that snippet
                let v = value.borrow();
                match v.typ() {
                    $obj_type => {
                        Ref::map(v, |v| {
                            v.as_any().downcast_ref::<$name>().expect(
                                concat!("failed to downcast ", stringify!($name))
                            )
                        })
                    }
                    _ => panic!(concat!("tried to downcast {} as ", stringify!($name)), v.typ()),
                }
            }

            pub fn [<is_e $lowercase_name >](value: &EObjRef) -> bool {
                let v = value.borrow();
                match v.typ() {
                    $obj_type => true,
                    _ => false
                }
            }
        }
    };
}


