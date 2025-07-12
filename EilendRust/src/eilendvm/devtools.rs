use crate::eilendvm::chunk::{ChunkConstant, CodeChunk};
use crate::eilendvm::object::base_object::{EObj, EObjRef, EObjTyp};
use crate::eilendvm::object::bool_object::as_ebool;
use crate::eilendvm::object::float_object::as_efloat;
use crate::eilendvm::object::func_object::as_efunc;
use crate::eilendvm::object::int_object::as_eint;
use crate::eilendvm::object::plain_object::as_obj;
use crate::eilendvm::object::str_object::as_estr;
use crate::eilendvm::opcodes::OpCode;
use crate::eilendvm::value_stack::ValueStack;

pub fn print_chunk(chunk: &CodeChunk) {
    println!("Code:");
    chunk.get_ops().iter().enumerate().for_each(|(i, op)| {
        match chunk.get_lineno(i) {
            Some(lineno) => print!("LN{:0>3} | {:0>4} | ", lineno, i),
            None => print!("      | {:0>4} | ", i),
        }
        print_op(op, chunk);
        println!();
    });
    println!("Constants ({}):", chunk.get_constants().len());
    chunk.get_constants().iter().enumerate().for_each(|(i, constant)| {
        print!("{: <4} => ", i);
        print_constant(constant);
        println!();
    })
}

pub fn print_op(op: &OpCode, chunk: &CodeChunk) {
    match op {
        OpCode::Nop =>
            print!("NOP"),
        OpCode::LoadConst(index) => {
            print!("LOAD_CONST\t{} (", index);
            print_constant(chunk.get_const(*index));
            print!(")");
        },
        OpCode::DebugPrintStack =>
            print!("DBG_PRINT_STACK"),
        OpCode::Echo =>
            print!("ECHO"),
        OpCode::PushBool(value) =>
            print!("PUSH_BOOL\t{}", value),
        OpCode::PushNull =>
            print!("PUSH_NULL"),
        OpCode::StoreGlobal(index) => {
            print!("STORE_GLOBAL\t{} (", index);
            print_constant(chunk.get_const(*index));
            print!(")");
        },
        OpCode::LoadGlobal(index) => {
            print!("LOAD_GLOBAL\t{} (", index);
            print_constant(chunk.get_const(*index));
            print!(")");
        },
        OpCode::JumpIfFalse(amount) =>
            print!("JUMP_IF_FALSE\t{}", amount),
        OpCode::JumpIfTrue(amount) =>
            print!("JUMP_IF_TRUE\t{}", amount),
        OpCode::Jump(amount) =>
            print!("JUMP\t\t{}", amount),
        OpCode::Call(arg_count) =>
            print!("CALL\t{}", arg_count),
    }
}

pub fn print_constant(chunk_constant: &ChunkConstant) {
    match chunk_constant {
        ChunkConstant::Str(s) => print!("'{}'", s),
        ChunkConstant::Int(i) => print!("{}", i),
        ChunkConstant::Float(f) => print!("{}", f),
    }
}

pub fn print_value(value: &EObjRef) {
    match as_obj(value).typ() {
        EObjTyp::INT => print!("<Int: {}>", as_eint(value).get_value()),
        EObjTyp::STR => print!("<Str: {}>", as_estr(value).get_value()),
        EObjTyp::FLOAT => print!("<Float: {}>", as_efloat(value).get_value()),
        EObjTyp::PLAIN => print!("<Obj>"),
        EObjTyp::BOOL => print!("<Bool: {}>", as_ebool(value).get_value()),
        EObjTyp::NULL => print!("<Null>"),
        EObjTyp::FUNC => print!("<Func: {}", as_efunc(value).get_value().name)
    }
}

pub fn print_stack(stack: &ValueStack) {
    println!("Stack:");
    stack.iter().enumerate().for_each(|(i, value)| {
        if i + 1 == stack.len() {
            print!("-> ");
        } else {
            print!("   ");
        }
        print_value(&value);
        println!();
    })
}
