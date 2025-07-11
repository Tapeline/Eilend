#[macro_export]
macro_rules! vm_panic {
    ($vm: expr, $cause: expr) => {
        panic!(
            "VM has crashed\nAt instr {} (line {})\n{}",
            $vm.ip - 1, $vm.get_current_line(), $cause
        )
    };
}


#[macro_export]
macro_rules! assert_that {
    ($vm: expr, $expr: expr) => {
        if !$expr {
            //panic!(
            //    "VM has crashed\nAt instr {} (line {})\nAssertion failed: {}",
            //    (self.ip), (self.get_current_line()), stringify!($expr)
            //)
            vm_panic!($vm, format!("Assertion failed: {}", $expr));
        }
    }
}


#[macro_export]
macro_rules! pop_stack {
    ($vm: expr) => {
        if $vm.value_stack.len() > 0 {
            $vm.value_stack.pop()
        } else {
            vm_panic!($vm, "Stack underflow");
        }
    }
}