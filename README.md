# **Doc for Social Computing Index**

Social Computing Index 代码说明

# **项目介绍**

该项目以 CSRankings 为设计模板、代码框架，设计出了 Social Computing Index 网站。SCI网站是基于一些社交计算的期刊对世界各国的高校、科学机构的成就做出排序，同时也给出了每一个作者的发表文章数目、指标得分。



# **代码说明**

分为两部分，一部分是**网站源代码修改**，另一部分是**dblp数据处理。**下面分别说明：



## 网站源代码修改
**我们的网站源代码： https://github.com/sds131/csranking**

前端显示基本上与 CSRankings 无异，除了前端的部分文字、图表显示。

Social Computing Index 和 CSRankings 相比，发生变化的是这几个文件：                 ![img](https://docimg2.docs.qq.com/image/T_7vsVrEMPgQmNTIToBjDw.png?w=1280&h=800)        

其中 country-info.csv、csrankings-*.csv、csranking.ts、index.html、util/csrankings.py 是需要我们修改的，csranking.js、csranking.min.js 等文件可以通过“make”指令自动生成。

- country-info.csv：存放我们在“dblp数据处理——作者匹配&大学列表更新”这一步得到的高校机构的“institution”、“region”、“countryabbrv”信息。注意：原来CSRankings中就存在的美国大学不能添加进去，否则会出现bug。
- csrankings-*.csv：csrankings-0-9.csv 存放我们在“dblp数据处理——爬虫代码”这一步得到的作者“name”、“affiliation”信息。csrankings-a-z.csv 无需我们修改，存放的信息为“csrankings-0-9.csv 所有作者信息汇总后按字母表顺序进行切分”，可以通过“make”指令执行。
- csranking.ts：typescript 语言的前端代码，修改（增加、减少）期刊种类时，需要修改。
- index.html：html 语言的前端代码，修改（增加、减少）期刊种类时，需要修改。
- util/csrankings.py：处理 dblp 数据的代码，修改（增加、减少）期刊种类时，需要修改。



### **服务器部署**

在 **/ranking** 文件夹中打开一个终端，执行命令行:

**python -m http.server 端口号**（如8111）

然后访问即可。若在本机部署，可直接用浏览器访问 127.0.0.1:8111



## **dblp数据处理**

**github地址：** https://github.com/sds131/SCI （即本仓库）


### **爬虫代码**

#### TCSS、SocNet

代码在 **/csranking/csranking.py** 中，代码说明如下：

- **get_urls(filepath)** : **filepath** 为 dblp 每个期刊初始地址（每一卷的网址）的集合——**journal****_xxx.txt** 的文件地址，通过读取 txt文件来爬虫。输出**urlxxx.csv，其中包含每一篇文章的源网址。**每次更新时，只需要写新的网址到文件 journal_xxx.txt 里即可，旧的可以删去。输出文件 **url_xxx.csv**。
- **get_affiliations_xxx(filepath)** : **filepath为url_xxx.csv文件地址，其中包含每一篇文章的源网址。**对具体期刊网站的爬虫代码。需要根据论文原网站（ieee、acm等）前端设计写出特定的代码。运行**get_affiliations_xxx(filepath)**函数，遍历**url_xxx.csv**中 **paper_url**，得到每一篇文章的作者名字、作者单位信息。其中论文源网站的作者名字和dblp的作者名字不是完全一致，无法直接作为最后的“name”，需要后续处理。作者单位也是复杂的字符串，不适合作为最后的“affiliation”。输出文件 **raw_author.csv**。
- **get_unique(filepath)** : **filepath** 为 dblp 每个期刊的初始地址（每一卷的网址）的集合——**journal_xxx.txt** 的文件地址。在DBLP中获取作者的特定名称，如：Fei-Yue Wang 0001，其中带000x表示有重名现象，需要加上数字加以区分。由于这一步已经使用了dblp中作者的特定名称，所以无需再往 dblp_aliases.csv 中添加作者别名信息。输出文件**author_unique.csv**。
- **手动修改**：由于论文网址丢失、部分作者无单位等原因，raw_author.csv可能不完整，需要手动将 raw_author.csv 和 author_unique.csv 进行比对，补充并修改 raw_author.csv，使得 raw_author.csv 和 author_unique.csv 行数一致。同时由于 author_unique.csv 的 author 字段正是 dblp 的作者姓名标识符，补充修改 raw_author.csv 后，需要将 author_unique.csv 中的 author 字段代替 raw_author.csv 中的 name 字段，这步可以直接复制粘贴。得到文件 **author_modified1.csv**。
- **disambiguation(filepath1,filepath2)** :  **filepath1** 为 dblp 每个期刊的初始地址（每一卷的网址）的集合——**journal_xxx.txt** 的文件地址。 **filepath2** 为**author_modified1.csv**。dblp的作者页面中存在需要消歧的作者页面，dblp无法分辨一些具有相同名字的作者，而这些作者也没有向dblp表明自己的准确身份，所以为了系统的准确，需要删除这些有争议和身份不明的作者信息。filepath1为**journal_xxx.txt** 的文件地址**，**filepath2 为 **author_modified1.csv** 的文件地址，通过 **journal_url** 遍历dblp的作者页面，**author_modified1.csv** 中将那些作者页面为 **disambiguation page** 的作者信息删除。输出文件 **author_modified2.csv**。
- **手动修改：**手动修改author_affiliation字符串，比如"Chinese Academy of Sciences"，会有人写成"Chinese **Academic** of Sciences"或者"Chinese Academy of **Science**"，这种错误需要我们自行确认手动修正。这步可以反复使用接下来的normalize(filepath1,filepath2)，根据 unnormlize.csv 反馈的信息对 author_modified.csv、 country-info.csv 进行修改得到最后的 author_modified.csv。
- **normalize(filepath1,filepath2) :** filepath1 为 **country-info.csv**，里面包含了各个大学机构的名称、大洲、国家信息，filepath2 为 **author_modified.csv**。将 country-info.csv 的大学机构名称字符串和 author_modified.csv 中的 affiliation 字符串进行字符串匹配，若 author_modified.csv 中的 affiliation 字符串中包含 country-info.csv 中的大学机构名称字符串，则将该作者的单位设为 country-info.csv 中的对应的大学机构名称。输出**normalize.csv、unnormalize.csv。**
- **duplicate(filepath) :** filepath 为 **normalize.csv** 的文档地址，需要对 **normalize.csv** 的作者信息进行去重，同一个作者只保留他最近最新工作的单位。输出**author.csv**。
- 将 author.csv 拷贝到 csrankings-*.csv。
- 修改前端 csrankings.ts，index.html 代码、修改util/csrankings.py的代码
- "make update-dblp", "make" 



#### TSC

代码在 **/crawl** 中，说明如下：

先运行 `mycrawler_address.py`， 再运行 `mycrawler_author_tsc.py`

* `mycrawler_address.py`：通过存在 **/crawl/journals** 中的 **ori_dblp_tsc.csv** （dblp中的会议导引链接，每一条链接都是一期期刊/会议的所有文章列表）来爬取每篇文章的原始 url。输出文件 **/crawl/journals/urls_tsc.csv**
* `mycrawler_author_tsc.py`：通过前面爬取的原网址，爬取该论文的作者信息。输出文件 **authors_tsc.csv**

* 随后可以用前面提到的 `手动修改`和 `normalize()` 函数来进行同样的操作.

（后续会改成统一的接口）

### **作者学校、地点的统一化（Normalize）**

根据前面的爬虫代码说明，可以得到每个期刊的原始作者信息列表 `normalize_authors_xxx.csv` 和 `unnormalize_authors_xxx.csv`。请将这些文件移动到 **/update_database** 

（后续会改成统一的接口）



### **作者匹配&大学列表更新**

代码在 **/update_database** 中。匹配：用新获取的作者和学校，去匹配已有学校，以获得标准化的 作者-机构。若不存在，则可能会将新的学校加入大学列表中。

#### **更新方法**

1、首先请确保在 **/update_database** 下有以下文件：

`normalize_author_xxx.csv`

`unnormalize_author_xxx.csv`

`enged-country-info-full.csv`

`us-university-info.csv`

`/json/country-full-info.json`

`/json/country-abbr.json`

`/json/continent-info.json`

`/json/dict-enged-university-info.json`

2、在这个文件夹中运行命令行 `make country_info.csv`。

3、用生成的 `country-info.csv` 替换网站源代码中的同名文件。

4、将生成的 `author-affiliations.csv` 中的所有姓名追加到网站源代码的 `csrankings-0.csv` 中（可以与原来的条目有重复）

5、在网站源代码中执行 `make` 即可。随后可以部署服务器。



#### **make文件说明** 

* make enged-country-info-full-new.csv

  1. 运行 **author_match1.py**，做初步匹配

  2. 运行 **author_match2.py** (这一步调用了谷歌（中国）翻译接口，将非英文的大学姓名翻译成英文。请确保科学上网处于**关闭状态**，否则会出现接口使用失败的情况）

     1和2运行后生成文件 

     * **not-matched-author.csv**，内容是本次运行后未匹配的作者信息。

  3. 运行 **university_complement.py**，生成文件如下：

     * **complement-university-info1.csv**，内容是本次补充的大学+所在的大洲和国家

     * **not-university-name.csv**，内容是不考虑加入我们大学列表的机构名称

  4. 运行 **concatenate.py**。生成
     * **enged-country-info-full-new.csv**，是最新的完整的大学列表
     * **dict-enged-university-info.csv**，原大学名-翻译后的大学名 键值对。

  5. **重复1次**步骤1、2，生成如下文件：

     * **author-affiliations.csv**，即本次数据补充后的新作者匹配结果

     * **not-matched-author.csv**，本次数据的不匹配结果。这里面的作者暂不加入我们的网站考虑范围（大多不是学校）

* make country-info.csv
  1. 运行 **./filter_american_schools.py**，过滤掉一些美国大学姓名（不过滤则会在网站中出错。这部分学校的列表在 **us-university-info.csv** 中。生成文件：
     * **country-info.csv**，最新的大学列表。用法前面讲到了。
  2. **mv enged-country-info-full-new.csv enged-country-info-full.csv**。文件更名。



#  
