#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  vector<int> res = {1, 2, 3, 4, 5, 6};
  int n;
  cin >> n;
  int r = n % 30;
  for (int i = 0; i < r; i++) {
    int j = i % 5;
    swap(res[j], res[j+1]);
  }
  for (int i = 0; i < 6; i++) {
    cout << res[i];
  }
  cout << endl;
  return 0;
}
