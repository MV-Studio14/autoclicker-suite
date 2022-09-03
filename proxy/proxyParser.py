def parse(data, port, origin):
    print(f"[{origin}:{port}] {data[:100].encode('hex')}")