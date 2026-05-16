# 1. Pastikan kamu di branch yang bener dulu
git branch
# kalau belum di branch kamu, pindah dulu:
git checkout feat/cli    # atau branch kamu

# 2. Cek file apa yang belum di-commit
git status
# harusnya cli.py dan sorting.py muncul sebagai "Untracked files"

# 3. Add file baru
git add src/modules/cli.py

# atau sekaligus semua yang belum ke-add:
git add .

# 4. Commit
git commit -m "feat(cli): tambah CLI interaktif dan sorting laporan"

# 5. Push ke GitHub
git push origin feat/cli    # ganti feat/cli dengan nama branch kamu