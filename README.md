# Custom Ruleset for sing-box

A curated collection of [sing-box](https://github.com/SagerNet/sing-box) rule-sets for major Chinese services, designed for direct routing.

## Features

- Covers major Chinese video, social, shopping, search, travel, and tech services
- Uses a bundled `sing-geosite` submodule for rule-set data
- Generates absolute-path `rules.json` automatically via Python script
- Supports Windows, Linux, and macOS

## Included Services

| Category | Services |
|----------|----------|
| Video | bilibili, iqiyi, youku, acfun |
| Social / Content | tencent, sina, douyin, kuaishou, xiaohongshu, zhihu, douban |
| Search / Tools | baidu, sogou, qihoo360, xunlei |
| Shopping | alibaba, jd |
| Cloud / Tech | aliyun, huawei, xiaomi |
| Travel / Lifestyle | meituan, didi, eleme, ctrip |
| Finance / Others | eastmoney, 58tongcheng, netease, ximalaya |

## Usage

### Clone with submodule

```bash
git clone --recurse-submodules https://github.com/chucongqing/custom-ruleset-for-sb.git
```

If already cloned without submodules:

```bash
git submodule update --init --recursive
```

### Generate `rules.json`

The repository does not include `rules.json` directly. Generate it from the template:

```bash
python generate-rules.py
```

Or use `make`:

```bash
make generate
make all    # same as make generate
```

This produces `rules.json` with absolute paths to the `sing-geosite` submodule.

### Update ruleset data

The `sing-geosite` submodule tracks the `rule-set` branch.

```bash
python update-ruleset.py
```

Or use `make`:

```bash
make update
```

### Available Makefile targets

```bash
make generate   # Generate rules.json from template
make update     # Update sing-geosite submodule to latest rule-set
make clean      # Remove generated rules.json
make all        # Run generate (default)
make help       # Show available targets
```

### Use with sing-box

Reference the generated `rules.json` in your sing-box configuration. Example rule-set entry:

```json
{
  "tag": "geosite-bilibili",
  "type": "local",
  "format": "binary",
  "path": "C:\\path\\to\\custom-ruleset-for-sb\\sing-geosite\\geosite-bilibili.srs"
}
```

On Linux/macOS the path will be POSIX-style:

```json
{
  "path": "/path/to/custom-ruleset-for-sb/sing-geosite/geosite-bilibili.srs"
}
```

### Use with v2rayN

v2rayN converts `geosite:xxx` style entries into sing-box rule-sets automatically. Converted entries from this ruleset:

```text
geosite:cn,
geosite:bilibili,
geosite:bilibili2,
geosite:bilibili-cdn,
geosite:bilibili-game,
geosite:iqiyi,
geosite:youku,
geosite:tencent,
geosite:tencent-dev,
geosite:tencent-games,
geosite:tencent-tme,
geosite:sina,
geosite:baidu,
geosite:alibaba,
geosite:alibaba-cn,
geosite:alibabacloud,
geosite:alibabacloud-cn,
geosite:aliyun,
geosite:aliyun-drive,
geosite:jd,
geosite:netease,
geosite:douyin,
geosite:kuaishou,
geosite:xiaohongshu,
geosite:zhihu,
geosite:meituan,
geosite:didi,
geosite:eleme,
geosite:ctrip,
geosite:sogou,
geosite:qihoo360,
geosite:xunlei,
geosite:ximalaya,
geosite:huawei,
geosite:huawei-dev,
geosite:huaweicloud,
geosite:xiaomi,
geosite:xiaomi-ai,
geosite:xiaomi-iot,
geosite:acfun,
geosite:douban,
geosite:eastmoney,
geosite:58tongcheng
```

And for IP:

```text
geoip:cn
```

Add these to a routing rule with outbound set to `direct`.

## License

MIT
