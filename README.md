# Doc for Social Computing Index

Social Computing Index 代码说明

## **项目介绍**

该项目以 CSRankings 为设计模板、代码框架，设计出了 Social Computing Index 网站。SCI网站是基于一些社交计算的期刊对世界各国的高校、科学机构的成就做出排序，同时也给出了每一个作者的发表文章数目、指标得分。

**我们的网站代码**： https://github.com/sds131/csranking

## 代码说明

分为两部分，一部分是**网站源代码修改**，另一部分是**dblp数据处理。**

### 网站源代码修改


前端显示基本上与 CSRankings 无异，除了前端的部分文字、图表显示。

Social Computing Index 和 CSRankings 相比，发生变化的是这几个文件：                 ![img](https://docimg2.docs.qq.com/image/T_7vsVrEMPgQmNTIToBjDw.png?w=1280&h=800)        

其中 `country-info.csv`、`csrankings-*.csv`、`csranking.ts`、`index.html`、`util/csrankings.py` 是需要我们修改的，`csranking.js`、`csranking.min.js` 等文件可以通过 `make` 指令自动生成。

- `country-info.csv`：存放我们在“dblp数据处理——作者匹配&大学列表更新”这一步得到的高校机构的 `institution`、`region`、`countryabbrv` 信息。注意：原来CSRankings中就存在的美国大学不能添加进去，否则会出现bug。
- `csrankings-*.csv`：`csrankings-0-9.csv` 存放我们在 “dblp数据处理——爬虫代码” 这一步得到的作者 `name`、`affiliation` 信息。`csrankings-a-z.csv` 无需我们修改，存放的信息为 `csrankings-0-9.csv` 所有作者信息汇总后按字母表顺序进行切分”，可以通过“make”指令执行。
- `csranking.ts`：typescript 语言的前端代码，修改（增加、减少）期刊种类时，需要修改。
- `index.html`：html 语言的前端代码，修改（增加、减少）期刊种类时，需要修改。
- `util/csrankings.py`：处理 dblp 数据的代码，修改（增加、减少）期刊种类时，需要修改。

### **服务器部署**

在 **/ranking** 文件夹中打开一个终端，执行命令行:

`python -m http.server 端口号`

如： `python -m http.server 8111`

然后访问即可。若在本机部署，可直接用浏览器访问 `127.0.0.1:8111`

## dblp数据处理

**github地址：** https://github.com/sds131/SCI （即本仓库）

### **爬虫代码**

位于 `/scranking` 文件夹中

#### 文件说明

`get_urls.py`：从 `dblp` 的网站获取每篇文章的 url 链接。

`crawler_xxx.py`：从每篇文章的 url 链接获取作者信息。`xxx` 代表期刊名称

`Makefile`：将上述文件打包运行

#### 使用说明

1. 将期刊每一卷的 url 放入 `/scranking/journals/ori_dblp_xxx.txt` 中。可以在 dblp 中搜索该期刊名称得到。

2. 在 `/scranking` 中打开终端，执行 `make get_authors ` 即可。

请确保电脑上已经安装了谷歌浏览器。

### **作者信息的规范化（normalization）**

#### 文件说明

`author_normalize.py`：将获取的作者信息规范化处理。其中有若干函数，说明如下：

- `get_unique(filepath)` ： 
  - `filepath` 为每个期刊的 dblp 网址所在文件，即 `ori_dblp_xxx.txt` 的文件路径。
  - 函数功能：在 dblp 中获取作者的特定名称，如：Fei-Yue Wang 0001，其中带000x表示有重名现象，需要加上数字加以区分。由于这一步已经使用了dblp中作者的特定名称，所以无需再往 dblp_aliases.csv 中添加作者别名信息。
  - 输出文件 `author_unique_xxx.csv`
- `disambiguation(filepath1, filepath2)` :  
  - `filepath1` 为每个期刊的 dblp 网址所在文件，即 `ori_dblp_xxx.txt` 的文件路径。
  -  `filepath2` 为 `author_modified1.csv` 的文件路径（在使用说明中会讲到这个文件）。
  - 函数功能：dblp的作者页面中存在需要消歧的作者页面，dblp无法分辨一些具有相同名字的作者，而这些作者也没有向dblp表明自己的准确身份，所以为了系统的准确，需要删除这些有争议和身份不明的作者信息。函数通过 `ori_dblp_xxx.txt` 遍历 dblp 的作者页面，将`author_modified1.csv` 中将那些作者页面为 **disambiguation page** 的作者信息删除。
  - 输出文件 `author_modified2.csv`。
- `normalize(filepath1,filepath2)`：
  * `filepath1` 为 `country-info.csv` 的文件路径，里面包含了**已经规范化的**各个大学机构的名称、大洲、国家信息，以此为标准来规范化各个作者的机构名称。
  * `filepath2` 为 `modified2_xxx.csv` / `modified3_xxx.csv` 的文件路径。
  * 函数功能：将 `country-info.csv` 的大学机构名称字符串和 `modified2_xxx.csv` 中的 `affiliation` 字符串进行字符串匹配。若 `modified2_xxx.csv` 中的 `affiliation` 字符串中包含 `country-info.csv` 中的大学机构名称字符串，则将该作者的单位设为 `country-info.csv` 中的对应的大学机构名称。
  * 输出文件 `normalize_author_xxx.csv`、`unnormalize_author_xxx.csv`
- `duplicate(filepath)` ：
  * `filepath` 为需要去重的文件的地址的文档地址，需要对作者信息进行去重，同一个作者只保留他最近最新工作的单位。
  * 输出 `modified3_xxx.csv`。

#### 使用说明

**代码中已经写好了遍历循环，因此每次运行代码都是对所有期刊做同样的处理，因此在手动修改的部分需要对每个期刊都手动修改。**

**以下说明中，未提到的参数无需修改**

1. 调用 `get_unique()` 函数：

   * 将 `author_normalize.py` 中的 `default` 变量值改为 `0`，对每个期刊执行 `get_unique()`。只需要将 `else` 以下的函数调用解注释后运行代码即可。

   * 本代码输出文件 `author_unique_xxx.csv`

2. 手动修改：

   * 由于论文网址丢失、部分作者无单位等原因，`authors_xxx.csv` 可能不完整，需要手动将 `authors_xxx.csv` 和 `author_unique_xxx.csv` 进行比对，补充并修改 `authors_xxx.csv`，使得 `authors_xxx.csv`和 `author_unique_xxx.csv` 行数一致。

   * 同时由于 `author_unique.csv` 的 `author` 字段正是 dblp 的作者姓名标识符，补充修改 `authors_xxx.csv` 后，需要将 `author_unique.csv` 中的 `author` 字段代替 `authors_xxx.csv `  中的 `name` 字段，这步可以直接整列复制粘贴。

   * 将修改后的 `authors_xxx.csv` 重命名为 `modified1.csv`

3. 调用 `disambiguationt()` 函数和 `normalize()` 函数：（）

   * 将 `get_unique()` 函数注释后，将这两个函数解注释，运行代码。

   * 本代码输出文件 `modified2_xxx.csv` 以及 `normalize_author_xxx.csv`、`unnormalize_author_xxx.csv`

4. 手动修改： 

   * 手动修改  `modified2_xxx.csv` 中的 `affiliation` 字段。比如 "Chinese Academy of Sciences"，可能会被写成 "Chinese **Academic** of Sciences" 或者 "Chinese Academy of **Science**"，这种错误需要我们自行确认手动修正。这一步进行的时候，可以根据观察 `unnormalize_author_xxx.csv` 中的 `affiliation ` 字段，来看哪些学校被误写，随后在 `modified2_xxx.csv` 中改成正确的。

   * 这步可以反复使用 `normalize()`，即修改一次之后，再调用 `normalize()` 函数重新匹配大学，随后根据 `unnormlize_author_xxx.csv` 反馈的信息对 `modified2_xxx.csv` 进行修改。

5. 去重、最终匹配：

   * 完成以上步骤后，调用 `duplicate()` 和 `normalize()` 函数，同样是在 `else` 部分解注释，运行代码。
   * 本代码输出文件 `modified2_xxx.csv` 以及 `normalize_author_xxx.csv`、`unnormalize_author_xxx.csv`，后两者将用于数据库更新。

### **作者匹配&大学列表更新**

代码位于在 `/update_database` 

匹配：用新获取的作者和学校，去匹配已有学校，以获得规范化的作者信息；若不存在，则可能会将新的学校加入大学列表中。

#### **文件说明** 

由于更新是使用 `Makefile` 全自动更新的，故只讲解 `Makefile` 中的代码。

* make enged-country-info-full-new.csv

  1. 运行 `author_match1.py`，做初步匹配

  2. 运行 `author_match2.py` (这一步调用了谷歌（中国）翻译接口，将非英文的大学姓名翻译成英文。请确保科学上网处于**关闭状态**，否则会出现接口使用失败的情况）

     1和2运行后生成文件 

     * `not-matched-author.csv`，内容是本次运行后未匹配的作者信息。

  3. 运行 `university_complement.py`，生成文件如下：

     * `complement-university-info1.csv`，内容是本次补充的大学+所在的大洲和国家

     * `not-university-name.csv`，内容是不考虑加入我们大学列表的机构名称

  4. 运行 `concatenate.py`。生成

     * `enged-country-info-full-new.csv`，是最新的完整的大学列表
     * `dict-enged-university-info.csv`，原大学名-翻译后的大学名 键值对。

  5. **重复1次**步骤1、2，生成如下文件：

     * `author-affiliations.csv`，即本次数据补充后的新作者匹配结果

     * `not-matched-author.csv`，本次数据的不匹配结果。这里面的作者暂不加入我们的网站考虑范围（大多不是学校）

* make country-info.csv

  1. 运行 `./filter_american_schools.py`，过滤掉一些美国大学姓名（不过滤则会在网站中出错。这部分学校的列表在 `us-university-info.csv` 中。生成文件：
     * `country-info.csv`，最新的大学列表。用法前面讲到了。
  2. `mv enged-country-info-full-new.csv enged-country-info-full.csv`。文件更名。

#### **使用说明**

1、首先请确保在 `/update_database` 下有以下文件：

* `normalize_author_xxx.csv`	
* `unnormalize_author_xxx.csv`
* `enged-country-info-full.csv`
* `us-university-info.csv`
* `/json/country-full-info.json`
* `/json/country-abbr.json`
* `/json/continent-info.json`
* `/json/dict-enged-university-info.json`

2、在这个文件夹中运行命令行 `make country_info.csv`

3、用生成的 `country-info.csv` 替换网站源代码中的同名文件。

4、将生成的 `author-affiliations.csv` 中的所有姓名追加到网站源代码的 `csrankings-0.csv` 中（可以与原来的条目有重复）

5、在网站源代码中执行 `make` 即可。随后即可部署服务器。





