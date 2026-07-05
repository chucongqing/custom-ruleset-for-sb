# Custom Ruleset for sing-box

A curated collection of [sing-box](https://github.com/SagerNet/sing-box) rule-sets for major Chinese services, designed for direct routing.

## Features

- Covers major Chinese video, social, shopping, search, travel, and tech services
- Uses relative paths to the bundled `sing-geosite` submodule
- Includes convenient update scripts for both Bash and PowerShell

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

### Update ruleset data

The `sing-geosite` submodule tracks the `rule-set` branch.

**Bash / Git Bash:**

```bash
bash update-ruleset.sh
```

**PowerShell:**

```powershell
.\update-ruleset.ps1
```

### Use with sing-box

Reference the `rules.json` file in your sing-box configuration. The rule-sets inside use relative paths like:

```json
{
  "tag": "geosite-bilibili",
  "type": "local",
  "format": "binary",
  "path": "sing-geosite\\geosite-bilibili.srs"
}
```

Make sure the `sing-geosite` directory is present alongside `rules.json` in your sing-box working directory.

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
