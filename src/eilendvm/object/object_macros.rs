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
macro_rules! eobj_common_converters {
    ($name: ident, $lowercase_name: ident, $obj_type: expr, $value_t: ty) => {
        paste::item! {
            pub fn [< v_ $lowercase_name >](value: $value_t) -> $name {
                $name {
                    table: Table::new(),
                    value
                }
            }

            pub fn [< v_ $lowercase_name _box >](value: $value_t) -> EObjDyn {
                Box::new($name {
                    table: Table::new(),
                    value
                })
            }

            pub fn [< as_e $lowercase_name >](value: &EObjDyn) -> &$name {
                match value.typ() {
                    $obj_type =>
                        value.as_any().downcast_ref::<$name>().expect(
                            concat!("failed to downcast ", stringify!($name))
                        ),
                    _ => panic!("tried to downcast {} as {}", value.typ(), stringify!($name))
                }
            }

            pub fn [< as_e $lowercase_name _mut >](value: &mut EObjDyn) -> &mut $name {
                match value.typ() {
                    $obj_type =>
                        value.as_any_mut().downcast_mut::<$name>().expect(
                            concat!("failed to downcast {}", stringify!($name))
                        ),
                    _ => panic!("tried to downcast {} as {}", value.typ(), stringify!($name))
                }
            }
        }
    };
}
