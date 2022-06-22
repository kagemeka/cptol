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


    let size_a: usize = sc.scan();
    let size_b: usize = sc.scan();
    let m: usize = sc.scan();
    let mut g = vec![];
    for _ in 0..m {
        let u: usize = sc.scan();
        let v: usize = sc.scan();
        g.push((u, v));
    }
    let max_match = hopcroft_karp(size_a, size_b, &g);
    writeln!(out, "{:?}", max_match.iter().filter(|v| v.is_some()).count()).unwrap();
}


/// Max Cardinal match on bipartite graph, ford fulkerson.
/// O(VE)
/// references
/// - https://en.wikipedia.org/wiki/Maximum_cardinality_matching
/// - https://ei1333.github.io/luzhiled/snippets/graph/bipartite-matching.html
/// - https://ei1333.github.io/algorithm/bipartite-matching.html
/// - https://onlinejudge.u-aizu.ac.jp/solutions/problem/GRL_7_A/review/5630283/ngtkana/Rust
/// - https://onlinejudge.u-aizu.ac.jp/solutions/problem/GRL_7_A/review/4329190/sansen/Rust
pub fn ford_fulkerson(size_a: usize, size_b: usize, g: &[Vec<usize>]) -> usize {
    fn dfs(g: &[Vec<usize>], pair: &mut [Option<usize>], visited: &mut [bool], u: usize) -> bool {
        visited[u] = true;
        for &v in g[u].iter() {
            if !pair[v].map_or(true, |v| !visited[v] && dfs(g, pair, visited, v)) { continue; }
            pair[v] = Some(u);
            pair[u] = Some(v);
            return true;
        }
        false
    }
    let n = g.len();
    assert_eq!(n, size_a + size_b);
    let mut pair = vec![None; n];
    for i in 0..size_a {
        if pair[i].is_some() { continue; }
        dfs(g, &mut pair, &mut vec![false; n], i);
    }
    pair.iter().take(size_a).filter(|v| v.is_some()).count()
}


/// Max Cardinal match on bipartite graph, hopcroft karp.
/// O(E\sqrt{V})
/// references
/// - https://en.wikipedia.org/wiki/Maximum_cardinality_matching
/// - https://misteer.hatenablog.com/entry/hopcroft-karp
/// - https://tjkendev.github.io/procon-library/python/max_flow/hopcroft-karp.html
/// - https://ei1333.github.io/algorithm/bipartite-matching.html
/// - https://www.youtube.com/watch?v=lM5eIpF0xjA
/// - https://judge.yosupo.jp/submission/6963
pub fn hopcroft_karp(size_a: usize, size_b: usize, g: &[(usize, usize)]) -> Vec<Option<usize>> {
    let bfs = |g: &[Vec<usize>], matched: &[bool], pair_a: &[Option<usize>]| -> Vec<usize> {
        let mut que = std::collections::VecDeque::new();
        let mut level = vec![std::usize::MAX; size_b];
        for u in 0..size_b {
            if matched[u] { continue; }
            level[u] = 0;
            que.push_back(u);
        }
        while let Some(u) = que.pop_front() {
            for &v in g[u].iter() {
                if let Some(u2) = pair_a[v] {
                    if level[u2] <= level[u] + 1 { continue; }
                    level[u2] = level[u] + 1;
                    que.push_back(u2);
                }
            }
        }
        level
    };

    fn dfs(
        g: &[Vec<usize>],
        level: &[usize],
        it: &mut [usize],
        pair_a: &mut [Option<usize>],
        matched: &mut [bool],
        u: usize,
    ) -> bool {
        for (i, &v) in g[u].iter().enumerate().skip(it[u]) {
            it[u] = i + 1;
            if !pair_a[v].map_or(true, |u2| {
                level[u2] == level[u] + 1 && dfs(g, level, it, pair_a, matched, u2)
            }) { continue; }
            pair_a[v] = Some(u);
            matched[u] = true;
            return true;
        }
        false
    }

    let mut t = vec![vec![]; size_b];
    for &(v, u) in g.iter() { t[u].push(v); } // v \in A, u \in B.
    let mut matched = vec![false; size_b];
    let mut pair_a = vec![None; size_a];

    loop {
        let level = bfs(&t, &matched, &pair_a);
        let mut it = vec![0; size_b];
        let mut updated = false;
        for u in 0..size_b {
            if !matched[u] { updated |= dfs(&t, &level, &mut it, &mut pair_a, &mut matched, u); }
        }
        if !updated { break; }
    }
    pair_a
}


/// Max Cardinal match on arbitral graph, blossom algorithm.
/// O(V^2E)
/// references
/// - https://en.wikipedia.org/wiki/Maximum_cardinality_matching
pub fn blossom() {
}
