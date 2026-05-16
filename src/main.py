elif pilihan == "7":
    print("\n--- LAPORAN HARI ---")

    if not selesai:
        print("⚠️ Belum ada pasien selesai hari ini")
        continue

    # Masukkan semua pasien selesai ke Linked List
    from src.modules.sorting import LinkedListPasien, insertion_sort_waktu_tunggu, selection_sort_no_antrian

    ll = LinkedListPasien()
    for p in selesai:
        ll.append(p)

    print("\nUrut berdasarkan:")
    print("  a. Waktu tunggu terlama (Insertion Sort)")
    print("  b. Nomor antrian (Selection Sort)")
    sub = input("Pilih (a/b): ").lower()

    if sub == "a":
        ll_sorted = insertion_sort_waktu_tunggu(ll)
        print("\n📋 Laporan - Waktu Tunggu Terlama | Big-O: O(n²)")
        print(f"{'No':<5} {'Nama':<20} {'Poli':<12} {'Prioritas':<10} {'Tunggu (s)'}")
        print("-" * 60)
        for p in ll_sorted.to_list():
            print(f"{p.no_antrian:<5} {p.nama:<20} {p.poli:<12} {p.prioritas:<10} {p.waktu_tunggu:.4f}")

    elif sub == "b":
        ll_sorted = selection_sort_no_antrian(ll)
        print("\n📋 Laporan - No Antrian | Big-O: O(n²)")
        print(f"{'No':<5} {'Nama':<20} {'Poli':<12} {'Prioritas':<10} {'Tunggu (s)'}")
        print("-" * 60)
        for p in ll_sorted.to_list():
            print(f"{p.no_antrian:<5} {p.nama:<20} {p.poli:<12} {p.prioritas:<10} {p.waktu_tunggu:.4f}")

    else:
        print("❌ Pilihan tidak valid")