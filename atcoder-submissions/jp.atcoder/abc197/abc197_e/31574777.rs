fn read_token<R, T>(reader: &mut R) -> Result<T, <T as std::str::FromStr>::Err>
where
    R: std::io::Read,
    T: std::str::FromStr,
{
    use std::io::Read;
    reader
        .by_ref()
        .bytes()
        .map(|c| c.unwrap() as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect::<String>()
        .parse::<T>()
}

// slow
fn read_stdin<T>() -> Result<T, <T as std::str::FromStr>::Err>
where
    T: std::str::FromStr,
{
    use std::io::Read;
    std::io::stdin()
        .lock()
        .by_ref()
        .bytes()
        .map(|c| c.unwrap() as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect::<String>()
        .parse::<T>()
}

pub struct ReadWrapper<R: std::io::BufRead> {
    reader: R,
    tokens: Vec<String>,
}

impl<R: std::io::BufRead> ReadWrapper<R> {
    /// let stdin = std::io::stdin();
    /// let mut reader = ReadWrapper::new(std::io::BufReader::new(stdin.lock()));
    /// let x = reader.read::<usize>();
    pub fn new(reader: R) -> Self {
        Self {
            reader,
            tokens: vec![],
        }
    }

    pub fn read<T: std::str::FromStr>(&mut self) -> Result<T, <T as std::str::FromStr>::Err> {
        while self.tokens.is_empty() {
            let mut buf = String::new();
            self.reader.read_line(&mut buf);
            self.tokens = buf
                // .rsplit_terminator('\n')
                // .split(' ')
                .split_whitespace()
                .rev()
                .map(String::from)
                .collect();
        }
        self.tokens.pop().unwrap().parse::<T>()
    }
}

pub fn locked_reader() -> ReadWrapper<std::io::StdinLock<'static>> {
    let stdin = Box::leak(Box::new(std::io::stdin()));
    ReadWrapper::new(stdin.lock())
}

/// Example
/// ```
/// use std::io::Write;
/// let writer = &mut locked_buf_writer();
/// writeln!(writer, "Hello, world!");
/// writer.flush().unwrap();
/// ```
pub fn locked_buf_writer() -> std::io::BufWriter<std::io::StdoutLock<'static>> {
    let stdout = Box::leak(Box::new(std::io::stdout()));
    std::io::BufWriter::new(stdout.lock())
}

pub fn fast_io() -> (
    ReadWrapper<std::io::StdinLock<'static>>,
    std::io::BufWriter<std::io::StdoutLock<'static>>,
) {
    (locked_reader(), locked_buf_writer())
}

// #[allow(warnings)]
fn main() -> Result<(), Box<dyn std::error::Error>> {
    use std::io::{BufRead, Write};
    let (mut reader, mut writer) = fast_io();
    // let stdin = std::io::stdin();
    // let mut reader = stdin.lock();
    // for _ in 0..1 << 20 {
    //     let mut buf = String::new();
    //     // read_stdin::<String>();
    //     reader.read_line(&mut buf);
    //     let tokens: Vec<String> = buf.split(' ').rev().map(String::from).collect();
    // }

    // let mut reader = ReadWrapper::new(stdin.lock());
    // for _ in 0..1 << 20 {
        // let a = reader.read::<String>()?;
        // writeln!(writer, "{}", a).unwrap();
        // writeln!(writer, "aaaaaaaaaaaaaaaaa").unwrap();
    // }
    let n = reader.read::<usize>()?;
    for _ in 0..n {
        let x = reader.read::<usize>()?;
        let c = reader.read::<usize>()?;
    }
    writer.flush().unwrap();

    Ok(())
}
