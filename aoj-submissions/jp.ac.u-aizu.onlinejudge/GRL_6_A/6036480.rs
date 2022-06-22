pub struct Scanner<R: std::io::Read> {
    reader: R,
}

impl<R: std::io::Read> Scanner<R> {
    /// let stdin = std::io::stdin();
    /// let mut sc = Scanner::new(stdin.lock());
    pub fn new(reader: R) -> Self { Self { reader: reader } }

    pub fn scan<T: std::str::FromStr>(&mut self) -> T {
        use std::io::Read;
        self.reader.by_ref().bytes().map(|c| c.unwrap() as char)
        .skip_while(|c| c.is_whitespace())
        .take_while(|c| !c.is_whitespace())
        .collect::<String>().parse::<T>().ok().unwrap()
    }
}


// #[allow(warnings)]
fn main() {
    use std::io::Write;
    let stdin = std::io::stdin();
    let mut sc = Scanner::new(std::io::BufReader::new(stdin.lock()));
    let stdout = std::io::stdout();
    let out = &mut std::io::BufWriter::new(stdout.lock());


    let n: usize = sc.scan();
    let m: usize = sc.scan();
    let mut g = vec![vec![]; n];
    for _ in 0..m {
        let u: usize = sc.scan();
        let v: usize = sc.scan();
        let cap: u64 = sc.scan();
        g[u].push((v, cap));
    }
    // let flow = dinic(&g, 0, n - 1);
    let flow = ford_fulkerson(&g, 0, n - 1);
    writeln!(out, "{}", flow).unwrap();
}


/// O(V^2 + Ef)
pub fn ford_fulkerson(g: &Vec<Vec<(usize, u64)>>, src: usize, sink: usize) -> u64 {
    let n = g.len();
    let mut rf = vec![vec![0; n]; n];
    for u in 0..n {
        for &(v, f) in g[u].iter() { rf[u][v] += f; }
    }
    let mut g: Vec<Vec<usize>> = vec![vec![]; n];
    for u in 0..n {
        for v in 0..n { if rf[u][v] > 0 { g[u].push(v); }; }
    }

    fn augment_flow(
        sink: usize,
        rf: &mut Vec<Vec<u64>>,
        g: &mut Vec<Vec<usize>>,
        visited: &mut Vec<bool>,
        u: usize,
        flow_in: u64,
    ) -> u64 {
        visited[u] = true;
        if u == sink { return flow_in; }
        let edges = g[u].clone();
        g[u].clear();
        let mut flow = 0;
        for &v in edges.iter() {
            if visited[v] || flow > 0 { g[u].push(v); continue; }
            flow = augment_flow(sink, rf, g, visited, v, std::cmp::min(flow_in, rf[u][v]));
            rf[u][v] -= flow;
            if rf[u][v] > 0 { g[u].push(v); }
            if flow == 0 { continue; }
            if rf[v][u] == 0 { g[v].push(u); }
            rf[v][u] += flow;
        }
        flow
    }

    // let mut visited = vec![false; n];
    let mut flow = 0;
    loop {
        // visited.fill(false);
        let mut visited = vec![false; n];
        let f = augment_flow(sink, &mut rf, &mut g, &mut visited, src, std::u64::MAX);
        if f == 0 { break; }
        flow += f;
    }
    flow
}



/// O(V^2E)
pub fn dinic(g: &Vec<Vec<(usize, u64)>>, src: usize, sink: usize) -> u64 {
    let n = g.len();
    let mut rf = vec![vec![0; n]; n];
    for u in 0..n {
        for &(v, f) in g[u].iter() { rf[u][v] += f; }
    }
    let mut g: Vec<Vec<usize>> = vec![vec![]; n];
    for u in 0..n {
        for v in 0..n { if rf[u][v] > 0 { g[u].push(v); }; }
    }
    let update_level = |g: &Vec<Vec<usize>>| {
        let mut level = vec![n; n];
        level[src] = 0;
        let mut que = std::collections::VecDeque::new();
        que.push_back(src);
        while let Some(u) = que.pop_front() {
            for &v in g[u].iter() {
                if level[v] != n { continue; }
                level[v] = level[u] + 1;
                que.push_back(v);
            }
        }
        level
    };

    fn flow_to_sink(
        sink: usize,
        rf: &mut Vec<Vec<u64>>,
        g: &mut Vec<Vec<usize>>,
        level: &Vec<usize>,
        u: usize,
        mut flow_in: u64,
    ) -> u64 {
        if u == sink { return flow_in; }
        let mut flow_out = 0;
        let edges = g[u].clone();
        g[u].clear();
        for &v in edges.iter() {
            if level[v] <= level[u] { g[u].push(v); continue; }
            let f = flow_to_sink(sink, rf, g, level, v, std::cmp::min(flow_in, rf[u][v]));
            rf[u][v] -= f;
            if rf[u][v] > 0 { g[u].push(v); }
            if rf[v][u] == 0 && f > 0 { g[v].push(u); }
            rf[v][u] += f;
            flow_in -= f;
            flow_out += f;
        }
        flow_out
    }


    let mut flow = 0;
    loop {
        let level = update_level(&g);
        if level[sink] == n { break; }
        flow += flow_to_sink(sink, &mut rf, &mut g, &level, src, std::u64::MAX);
    }
    flow
}
