pub trait IO {
    fn print(&mut self, s: &str) {
        todo!()
    }

    fn get_contents(&self) -> String {
        todo!()
    }
}

pub struct StdIO {}

impl IO for StdIO {
    fn print(&mut self, s: &str) {
        print!("{}", s);
    }

    fn get_contents(&self) -> String {
        panic!("Cannot get contents from StdIO")
    }
}


pub struct StrIO {
    pub output: String,
}

impl IO for StrIO {
    fn print(&mut self, s: &str) {
        self.output.push_str(s);
    }

    fn get_contents(&self) -> String {
        self.output.clone()
    }
}

impl StrIO {
    pub fn new() -> StrIO {
        StrIO {output: String::new()}
    }
}
