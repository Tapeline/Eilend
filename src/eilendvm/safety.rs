#[macro_export]
macro_rules! assert_that {
    ($expr: expr) => {
        if !$expr { panic!("Assertion failed: {}", stringify!($expr)); }
    }
}
