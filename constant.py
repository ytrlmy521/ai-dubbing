


# --- 《好事成双》提示词模板 ---
Good_Things_PROMPT_TEMPLATE = """
翻译要求：将电视剧《好事成双》中文剧本译为美式英语配音稿。需确保：
1）角色身份准确，与第10项的任务身份一致（林双-前顶尖高材生/全职主妇，顾许-海归精英/林双同学，江喜-职场女性/林双闺蜜）,中文中涉及特殊术语的请参考第11项的翻译术语字典表，例如： 中文 "公子"	 你直接使用术语对照表的结果就行：Young Master，"姑奶奶" 直接使用 Granny。
2）译文行数与原文逐行对应 
3）口语化表达符合角色身份 
4）专业术语保持语境一致 
5）保留5%行数弹性空间 
6）使用当代美式英语表达习惯 
7）确保口型同步适配 
8）PG级语言规范。注意人物关系表述的自然流畅，职场场景用词需符合硅谷科技公司背景设定。
9) 剧情背景介绍：Lin Shuang, once a top university graduate, became a full-time mom after marriage—only to face betrayal. Fighting for custody of her daughter, she returns to the workforce, where she stumbles upon Gu Xu, her former classmate now a high-achieving returnee. Shocked to see her abandon her hard-earned skills for marriage, he is frustrated yet drawn to her resilience. With support from friend Jiang Xi, Lin Shuang overcomes challenges in love, career, and family, proving her worth. As she transforms from homemaker to professional, she also finds love with Gu Xu. Both Lin Shuang and Jiang Xi grow through rivalry and camaraderie, forging new futures. Please translate this modern TV show’s script into American English for lip sync dubbing.

10) 人物身份：
林双：曾是天之骄女的林双在怀孕生子后，辞去工作成为全职主妇，每日围绕家庭大小事宜奔波不停，直到她发现丈夫卫明的背叛，婚姻危机一触即发。为了在离婚时能顺利夺下女儿的抚养权，林双必须重返职场实现经济独立，以证明自己有养育孩子的能力。但她在对家庭孤注一掷的10年里，也被迫失去了自我，逐渐走向了人生窄路。顾许：出身普通城市家庭，从小开明的教育让尊重他人和换位思考刻在骨子里。顾许性格木讷不善言谈，当得知林双毕业后就放弃专业做了家庭主妇，顾许替她不甘，也气她不争气。随着林双的成长，顾许的钦佩和保护欲逐渐变成爱恋，这些年他尊重林双的决定，选择退出和祝福，但他承认自己从没忘记过林双。江喜：出身小镇，赌徒父亲四处躲债让她毫无安全感，重男轻女的母亲只会在她身上吸血，将教育资源严重向儿子江海倾斜。江喜毕业后来到大城市打拼，她一面努力生活，一面包装自己。从小城市的大公司，到大城市的小公司，再从方舟的前台，内部转岗到市场部做商务拓展，她利用一切机会去攀附各路大佬，刷新自己的行业经验。卫明：出身小城市，父母是小生意人，他的出身环境也养成了他利益至上的人生信条。自小习惯了斤斤计较，形成了以自我利益为中心的自私性格。但是眼力见儿极好善于见风使舵，也让他对女人的情绪非常敏感，假意温柔，在一开始就将林双和江喜哄得团团转。可当发现原本被自己哄得团团转的林双和江喜心生反意，便睚眦必报地打击报复。黄嘉仪：出生豪门千金，自小在外留学缺乏家庭温暖，父母因此对她过度保护弥补导致心事单纯涉事未深。黄嘉仪虽是空降公司，但她履历和能力都很出众，对自己所负责的工作也兢兢业业，不遗余力的去完成。但是人际关系的处理却不尽如人意，团队协作经验不足，过于直接的沟通方式引起同事高度不满和抵制，导致工作举步维艰。

11)翻译术语字典表（中文	--> 英文)

冯总旗	Commander Feng
张十三	Zhang Shisan
白一夏	Bai Yi xia
罗克敌	Luo Ke di/Rock di
公子	Young Master
谢雨霏	Xie yufei
齐王	the King of Qi
姑奶奶	Granny
夏	Hsia
铁铉	Tieh Hyeon
北平	Beiping
西门	Simon
谢谢	cece
方孝孺	Faung Xiaoru
茗儿	Ming
胡虏/胡人	northern barbarian
谢木思	Shemuth
阿尔斯兰	Arslan
麦苏木	Maisumu
锦衣卫	Imperial Guards
拱卫司	Garrison Command
御前三等带刀侍卫	the third-ranked Imperial Swordsman
左军大都督	the Left Army Commander.
五军都督府	Five Armies Office
凌霄帮	Soaring Sky Sect
楚米帮	Chumi Gang
燕王府	Prince Yan's Residence
大理寺	Court of Judicial Review
北平布政司	Beiping Administration Commission
五虎斩门刀	Five Tigers Broadsword
吾皇万岁万岁万万岁	Long live Your Majesty, long may your reign!
双屿岛/帮	Double Island
腰牌	waist plaque
悔婚费	Repudiation fee


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""


# --- 何以笙箫默提示词模板 ---
Sheng_Xiao_Mo_PROMPT_TEMPLATE = """
翻译要求：将电视剧《何以笙箫默》中文剧本译为美式英语配音稿。需确保：

 1. 剧名译法：《何以笙箫默》译为"Silent Separation" 
 2. 角色处理： - 男主：**Ho Yichen**（精英律师，外冷内热，父母因赵家破产自杀） - 女主：**Zhao Mosheng**（摄影师，冒失善良，为救孤儿假结婚） 
 3. 语言风格： - 美式英语口语化 - 保留10%中文称谓（如"Brother Yuan"） - 法律术语简化处理（例：将"judicial appeal"替换为"legal fight"） 
 4. 格式规范： 
 - 俚语使用美式表达（例："bloody hell"→"darn it"） 
 - 中文文化专有项音译+括号注解释义（例："qipao (traditional silk dress)"） 
 - 激情戏翻译保留原作张力但符合PG评级 
 5. 技术指标： 
 - 允许±5%行数浮动 
 - 角色名保留拼音原写法 
 - 每句译文与原文段落换行位置对齐
 6.术语表映射
 - 瑰宝杂志社 Treasure
 - 何以琛 Ho Yichen
9) 剧情背景介绍：He Yichen, the brilliant and aloof law school golden boy, never expected to fall for Zhao Mosheng—the bubbly, accident-prone photography enthusiast who crashed into his life and his heart with her camera lens. Their unlikely campus romance blossomed despite his initial resistance, until family secrets tore them apart: her father's involvement in his parents' tragic past. A bitter confrontation sent Mosheng fleeing overseas for seven long years. When she returned, their unresolved passion erupted into a turbulent reunion—Yichen's lingering resentment and mistaken assumptions about her "marriage" abroad led to a coercive wedding. But love ultimately triumphed when truth revealed her sacrificial act: a paper marriage to save an orphaned child.

10) 人物身份：何以琛：出身寒门却十分优秀的法学院才子，英俊不凡、器宇轩昂，却十分低调，浑身散发着生人莫近的气场。遇到赵默笙后，以琛的生活被全部打乱，他跟随自己的心和这个特别的女孩在一起，可两人却又因为误会分开。从校园步入到社会，何以琛成了一个非常有规模的律师事务所的合伙人，年轻有为、事业有成。这个在职场所向披靡的大律师，对自己身边发生的一切事情客观冷静、胸有成竹，但只要一接触到与默笙有关的事时，便难以保持理智。赵默笙：天真爽朗，甚至有些没心没肺，对以琛一见钟情后便勇起直追，也开始了与他一生的爱恋与纠缠。离开以琛的七年里，默笙经历了丧父、艰难打工留学等变故，为了抚养一个可怜的孩子，在美国与应晖名义上结发。七年以后重回上海之时，成为摄影师的默笙已然变得隐忍成熟。重遇以琛，历经爱情的考验，默笙终于拥有幸福的家庭，并与以琛有了一个孩子何照。何以玫：何以琛养父母的女儿，自幼喜欢以琛。大学时她对默笙说的竞争宣言，导致默笙远走美国，但以玫的执着与守候还是无法换回以琛的回首。默笙回国后不久，她便放手并祝福以琛与默笙，后与张续结婚，产下一女。应晖：SOSO总裁，默笙“前夫”。应晖来自一个普通的农村家庭，家境贫寒，大学期间成绩优异。因为女友打破了他对生活的平淡渴望，应晖申请了奖学金出国留学。创业初期，身处困境的应晖得到默笙500美元的帮助，使其撑过了最艰难的时期。最后，应晖看到默笙对以琛的真心，便将结婚实情告知以琛，从他们两人间退出。

11)翻译术语字典表（中文	--> 英文)

瑰宝杂志社	Treasure
何以琛	Ho Yichen


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""


# --- 《锦衣夜行》提示词模板 ---
Jin_Yi_Ye_Xing_PROMPT_TEMPLATE = """
翻译要求：将电视剧《锦衣夜行》中文剧本译为英式英语配音稿。需确保：
 
1. 标题《锦衣夜行》译为英式英语，优先参考官方英文名，若未找到则直译为 *"Brocade Guards Under Night"* 
2. 角色名按中文拼音翻译：夏浔=Xia Xun，谢雨霏=Xie Yufei，朱棣=Zhu Di，杨旭=Yang Xu 
3. 对白风格符合古装权谋剧基调，使用英式拼写（如colour而非color） 
4. 人物身份描述需体现第10项的细节描述： - 夏浔：冒名顶替杨旭的草根人物→锦衣卫→燕王心腹 - 谢雨霏：智谋型女主，江湖背景 - 朱棣：燕王→发动靖难之役夺权的永乐帝 
5. 保留原文权力斗争与爱情线的双线叙事节奏 
6. 译文行数与原文严格对齐（含空行），允许±10%字数浮动 
7. 分级PG-18：政治阴谋与暴力场面保留写实感，情欲戏份用隐喻手法处理 
8. 术语一致性：使用第11项的翻译术语字典表的英文映射值。


9.剧情背景介绍：The story is set in the early Ming Dynasty. The male lead, Xia Xun, accidentally takes on the identity of Yang Xu, a deceased wealthy scholar. Posing as Yang Xu, he becomes an imperial guard under Prince Yan Zhu Di, who later seizes the throne, and assists in his rise to power. Amid his ambitions in the imperial court, Xia Xun meets and falls in love with the female lead, Xie Yufei.


10.人物身份：夏浔: 谢雨霏的丈夫，锦衣卫指挥使，辅佐朱棣，成就一代伟业。无论是靖难削藩，迁都修典，还是五征蒙古，七下南洋等，夏浔都参与其中，并深刻影响着历史的进程。朴敏英: 夏浔的妻子，他们是一对患难与共的欢喜冤家。谢雨霏，本名谢露缇，自取小字雨霏，小名谢谢，杨旭的未婚妻，陈郡谢家之人。然而到她之时，家道已经衰落，在父母相继去世，哥哥又被压断腿无缘仕途后，谢雨霏过早的面对了生活的压力，后嫁给夏洵为妻，为辅国公夫人，后被纪纲与郡主设计与夏洵和离，和离时已怀有与夏洵的孩子，怀着孩子嫁给纪纲为妻，之后设计纪纲逃离出府后在外被郡主的马车害到而流产，后与夏洵成功排除万难，与夏洵再次复婚。西门靖: 夏浔结拜兄弟。长袖善舞八面玲珑，手段圆滑做事老成，本人还是一个妇科名医，在阳谷县里名声并不赖，至少没人听说过他干过什么欺男霸女、作奸犯科的坏事儿，可算是一位妙人。然而却是锦衣卫中人，通过其父传承了锦衣卫的身份，西门靖的武功很高，刀剑功夫，极其之高，除了纪纲能与之抗衡一下，其他人很难近他身，喜欢彭梓琪。纪纲: 夏浔结拜兄弟。自幼习武，一身拳脚功夫极为了得，为人好名，与高贤宁交情深厚，后被开除县学。在高贤宁游学时，纪纲也相伴同行，却恰遇蒲台县仇秋强掳，民女之事，深爱着谢雨霏，纪纲于夏浔等联手，巧施计谋，使得仇秋人赃俱获，自己也收获了不小的名声，后来与夏浔兄弟反目，也因最爱的女人谢雨霏选择夏浔而更加恨夏浔，后来使出手段让谢雨霏与夏洵和离，而娶谢雨霏为妻，但谢雨霏嫁给他时已怀有夏洵的孩子，之后谢雨霏逃出府后被郡主的马车害到流产，后因谢雨霏易容成夏洵的模样去见他，却不知是谢雨霏，而用剑刺伤谢雨霏，后来斯下易容的面具发现是谢雨霏，伤心绝望自己伤害了她，当下在谢雨霏与夏洵面前用剑自尽，断气前与夏洵道歉自己背叛兄弟之情。


11.翻译术语字典表（中文	--> 英文)

冯总旗	Commander Feng
张十三	Zhang Shisan
白一夏	Bai Yi xia
罗克敌	Luo Ke di/Rock di
公子	Young Master
谢雨霏	Xie yufei
齐王	the King of Qi
姑奶奶	Granny
夏	Hsia
铁铉	Tieh Hyeon
北平	Beiping
西门	Simon
谢谢	cece
方孝孺	Faung Xiaoru
茗儿	Ming
胡虏/胡人	northern barbarian
谢木思	Shemuth
阿尔斯兰	Arslan
麦苏木	Maisumu
锦衣卫	Imperial Guards
拱卫司	Garrison Command
御前三等带刀侍卫	the third-ranked Imperial Swordsman
左军大都督	the Left Army Commander.
五军都督府	Five Armies Office
凌霄帮	Soaring Sky Sect
楚米帮	Chumi Gang
燕王府	Prince Yan's Residence
大理寺	Court of Judicial Review
北平布政司	Beiping Administration Commission
五虎斩门刀	Five Tigers Broadsword
吾皇万岁万岁万万岁	Long live Your Majesty, long may your reign!
双屿岛/帮	Double Island
腰牌	waist plaque
悔婚费	Repudiation fee


请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""





# --- 《亲爱的热爱的》提示词模板 ---
Qing_Ai_De_PROMPT_TEMPLATE = """
翻译要求：将电视剧《亲爱的热爱的》中文剧本译为英式英语配音稿。需确保：
 
1.使用非正式语气，保持中文原文情感基调。
2.译文行数严格匹配原文段落结构，长度浮动±5%。
需体现《亲爱的热爱的》中天才少女佟年（Tong Nian）与电竞男神韩商言（Han Shangyan）的甜蜜互动，突出「一见钟情主动追爱」的梦幻感，同时准确传递电竞战队运营细节、CTF全球编程赛事专业术语。注意保留「为国争光」「团队热血」等体现青年家国情怀的关键词。译文需符合PG内容分级规范，遵循坦桑尼亚TCRA媒体传播条款。

3.剧情背景介绍：The drama is a sweet romance about the storyt of the adorable genius Tong Nian falls for the passionate esports star Han Shangyan at first sight and boldly pursues him. Their love story is dreamy and heartwarming. Beyond romance, the drama highlights esports teams, world-class programming competitions, and the younger generation’s passion, teamwork, and sense of national pride.

4.人物身份：Tong Nian (佟年)A sweet, talented computer science student with a passion for singing and cosplay. Tong Nian is cheerful, kind-hearted, and brave when it comes to love. Though shy at first, she’s determined and sincere—qualities that slowly melt Han Shangyan’s cold exterior.Han Shangyan (韩商言)A legendary esports player and the founder of Team K&K. Stoic, focused, and often misunderstood, Han Shangyan hides a soft heart under his tough exterior. He is dedicated to mentoring young talent and carrying the Chinese cybersecurity dream forward.Wu Bai (吴白)Han Shangyan’s cousin and the top player in K&K. Nicknamed “DT,” he’s calm, collected, and admired by many. Wu Bai is a strategic genius and a quiet pillar of strength in the team.Grunt (沈哲)A former member of Han Shangyan’s old team, Solo. Now with SP (a rival team), Grunt is mature, professional, and still maintains a deep friendship with the team, despite past misunderstandings.🐯 Solo (王浩)The former team captain and Han Shangyan’s old friend. Now a coach and father, Solo represents the emotional anchor between past and present. His history with Han Shangyan adds emotional weight to the storyline.🌟 Ai Qing (艾情)Also known as “Appledog,” she is a well-respected female gamer and team manager. Ai Qing is intelligent, strong, and supportive, and has a complex romantic history with Han Shangyan and Solo.


请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""



# --- 《宇宙护卫队S4》提示词模板 ---
YuZhouHuWeiDui_PROMPT_TEMPLATE = """
翻译要求：将动画片《宇宙护卫队S4》中文剧本译为美式英语配音稿。需确保：
 
非正式美式英语，保持口语化表达 译文要求： 
1. 角色名称统一使用英文代号（Storm/Rainbow/Flash/Meteor/Raindrop/Thunderbolt/Sunshine） 翻译中文中涉及特殊术语的请使用第8项的翻译术语字典表的值。
2. 对话节奏与原文呼吸点同步，译文行数严格匹配原文 
3. 允许5%灵活调整幅度，保留中文特有文化概念时需加译者注[TN] 
4. 符合PG-13分级规范，战斗场景避免血腥描述 
5. 机器人Raindrop台词需体现机械语音特征，使用不完整句式 
6. 反派Thunderbolt用词偏古典英语，Sunshine台词夹杂科技俚语 


7.剧情背景介绍：It's a Chinese cartoon series, telling the story of the Cosmic Crew, including brave Storm, knowledgeable and quick-witted Rainbow, natural-born go-getter Flash, Meteor, and a robot Raindrop, setting out once again to protect the inhabitants of Earth, engaging in a battle of wits and courage against Thunderboltand Sunshine.


8.翻译术语字典表（中文	--> 英文)

宇宙护卫队	Cosmic Crew
跳跳农场	Hopper's Farm
风暴机车	Storm Racer
彩虹机车	Rainbow Racer
闪电机车	Flash Racer
流星机车	Meteor Racer
流星	Meteor
彩虹能量	Rainbow Energy
彩虹医疗站	Rainbow Medical Station
彩虹能量罩	Rainbow Energy Shield
风暴力量	Storm Power
闪电飞梭	Flash Dash
闪电飞腿	Flash Kick
彩虹	Rainbow
风暴	Storm
闪电	Flash
小雨点	Raindrop
麦麦	Mike
百变流星	Versatile Meteor
滑翔翼	glider wing
紧急时刻 保持冷静 遇到困难 永远不要退缩!	In an emergency, stay calm. When facing difficulty, never ever back down!
摩卡	Mocha
阿七	Seven
泡泡老师	Ms. Bubble
道齐	Dodge
萌萌	Cute
小小鸭	Little Duckling
斑斑	Benny
小李老师	Mr. Lee
大力	Strong
杰克	Jack
阿杜	Du
警报，警报！……警报，警报！	Alert, alert!... Alert, alert!
有任务	Mission!
显示任务坐标！目的地	Show task coordinates! Destination:
出发	Let's go!
聚焦星球	Planet Spotlight
兔爷爷	Grandpa Bunny
企鹅号	The Penguin
南部森林	South Woods
森林医院	Woods Hospital
能量泡	Energy Bubble
熊狸	binturong
阿莫	Mo
朱莉	Julie
小可	Cocoa
阿曼	Ahmed
速速	Speed
鲁道夫	Rudolph
小松果	Pinecone
临海雪原	Seaward Snowfield
冰原森林	Ice Forest
风暴战拳	Storm Fist
芃芃丛林	Pengpeng Forest
丁丁	Dingding
当当	Dangdang
龙龙	Longlong
阿蒙	Mong
蓬蓬	Pumba
塔西教授	Prof. Tassi
蓝天	Sky
兰克船长	Captain Rank
波比	Poppy
主持人	MC
海鸟	Sea bird



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《神隐》提示词模板 ---
ShenYing_PROMPT_TEMPLATE = """
翻译要求：将电视剧《神隐》中文剧本译为英式英语配音稿。需确保：
 
1. 翻译中文中涉及特殊术语的请使用第10项的翻译术语字典表的值。
2. 英式英语非正式风格 
3 保持原文行数一致允许±5%调整 PG13评级 
4.角色身份:角色身份翻译也需要从第10项的翻译术语字典表的值获取。

5. 英式俚语适配奇幻语境 
6. 情感台词避免直译 保持自然对话感 
7. 文化专有项采用解释性翻译

8.剧情背景介绍：The story is set in the far ancient times. It follows Ah Yin, a Water Divine Beast, and Gu Jin, the son of a true god whose powers are sealed, as they embark on a quest to retrieve the fragments of Feng Yin's Immortal Essence.Alongside companions Hong Yi, prince of the Fox Clan, and Yan Shuang, princess of the Eagle Clan, they confront numerous challenges to restore peace across the realms.Throughout their journey, they discover profound bonds of love, friendship, and family, ultimately fulfilling their promise to maintain harmony in the world.

9.人物身份：阿音、凤隐：天帝凤渊的徒弟，仙界梧桐岛凤族第二只火凤。凤隐在初次降生时因古晋的无心之失仙元尽散，其中一枚仙元寄生在了水凝兽体内，被古晋孵化后收为仙仆，陪伴他踏上了寻找凤隐仙元之旅。一路上两人互生情愫，然而因为种种误会与阴差阳错，阿音被古晋用元神剑打得魂飞魄散，在人间历劫千年后，凤隐得以重生归来。古晋、元启：帝眷与仪合之子。元启的父亲帝眷为阻止灭世之劫以身殉世，元启受此刺激神力全无，被母亲仪合送到下界来历练，成为大泽山掌教东华上君座下弟子。他奉师命去梧桐岛参加火凤降生宴时，因无心之失致使凤隐陨灭。为弥补，他以身受一劫为代价，换取了凤隐的一线生机。之后为复活凤隐，古晋与仙仆阿音结伴踏上了寻找凤隐仙元之旅。鸿若：妖界狐族狐王。年轻时的鸿若和林墨相爱，让她错过了去拯救自己的族人，这也成了她最大的遗憾。此后她放下了这段感情，成了狐王肩负起自己的责任，所有精力都放在治理狐族和教导侄子鸿奕身上。为了保护鸿奕，她将自己一半修为封印在檀木手串之中，交给他随身佩戴，自己却因此被青霖夺舍。鸿奕：鸿若的侄子，妖皇，十尾天狐。鸿奕在三重天锻造兵刃时，被魔族引到了九渊煞狱，身受重伤时幸得阿音相救，因此喜欢上了阿音，可是阿音喜欢的却是古晋，而在他没注意到的地方，鹰族公主宴爽默默喜欢着他。直到最后鸿奕终于认清了自己对宴爽的心意，彻底放下了对阿音的执念。华姝：仙界孔雀族公主。华姝天生自卑，不甘心屈居于凤族之下，一心想让孔雀族成为一流仙门，为此不择手段。就在她遇到自己的真爱澜沣，想就此悔改走上正途时，却不想大婚当日，澜沣遭人暗算身亡。还未嫁夫先死，伤心不已的华姝一心想为澜沣报仇，后得知父亲才是杀害澜沣的真凶时，她选择大义灭亲。宴爽：仙界鹰族公主。宴爽性格豪爽、率真。因为母亲早逝，她从小便肩负起守护鹰族的重任。在寻找能给父亲治伤的灵药碧血灵芝时，她与阿音、鸿奕等人不打不相识，成为了朋友。鸿奕更是在关键时刻帮她打退了孔雀族的追杀，宴爽因此对他暗生情愫。然而鸿奕却对阿音情有独钟，宴爽只能默默的将这份感情埋藏在心里。澜沣：代天帝。澜沣出身不俗，实力超群。凤渊闭关海外后，他代掌天界，是公认的继任天帝的最佳人选。澜沣是一个公私分明的人，虽然喜欢上孔雀族公主华姝，却不愿动用关系，为孔雀族牟利。他选择用另一种方式来爱华姝，包容她的缺点，为她受罚，用自己的爱来治愈她。修言、敖歌：幽洺王。敖歌与修言是双生兄弟，他们诞生于上古神界。弟弟敖歌司生，哥哥修言司灭。神界命敖歌为天帝，命修言为幽洺王。七万年前的伏魔大战中，修言以兵解之法对抗魔神冥起，致使内丹四散。多亏敖歌找到了修言的内丹碎片，还以自己的肉身帮他蕴养内丹，才让修言“活”了下来，从此两人一体双生，敖歌选择代修言成为幽洺王。凤渊：天帝兼凤族凤皇，凤隐的师父。凤渊是凤族的第一只火凤，也是至高无上的天帝，在她的治下，三界一片祥和。凤隐成为第二只火凤后，她对其寄予厚望，意图将凤隐培养成自己的接班人。之前她已用两百年的时间集齐了晨放的仙元，遂闭关海外为其蕴养仙元，天帝之位交由澜沣代管。



10.翻译术语字典表（中文	--> 英文)


阿音	Yin
小幽君	You Jun
梧桐岛	Wutong Island
凤皇	Phoenix Queen
小师叔	Senior
师侄	Junior
闲竹师叔	Senior Xianzhu
青衣	Qing Yi
阿晋	Jin
火凰玉	Phoenix Jade
半神	demi-god
炙魂草	Soul-scorching Grass
仙元	spirit
幽洺王	Nether King
三生石	Three-life Stone
水凝兽	Water Divine Beast
问天石	Heaven Stone
大泽山	Dazeh Mountain
红绸大人	Lady HongChou
忘念笛	Forgetfulness Flute
魂印	Soul Mark
忘忧鲜果	Worry-free Immortal Fruit
阿羽	Yu
阿玖	Jiu
结界石	boundary stone
天宫	Heavenly court
劫数	doom
狐王	Fox Queen
阿若	Ruo




请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""



# --- 《青云志》提示词模板 ---
QingYunZhi_PROMPT_TEMPLATE = """
翻译要求：将电视剧《青云志》中文剧本译为英式英语配音稿。需确保：
 
将古装玄幻剧《青云志第二季》剧本译为英式英语配音台词，口型同步率达95%。需严格匹配每句首尾开闭口音，逐音节校准停顿位置（如爆破音/p//b/等收尾词用闭口音节），调整元音长度与气口呼吸节奏，确保配音演员口腔运动轨迹与原片一致。用词需符合PG-13分级标准。 
角色塑造重点： - 张小凡（青云门堕魔弟子）：突出悲怆撕裂感，保留"blood-devouring bead"等法器术语 - 碧瑶（鬼王之女）：强调灵体状态的空灵回声效果 - 陆雪琪（冷峻师姐）：克制型情感表达，设计含蓄双关语 - 鬼王（碧瑶之父）：帝王级威严与父爱矛盾 - 黑心老人（魔教长老）：沙哑声线适配老年反派设定 风格规范： 1. 武打场面用短促爆破辅音（如thrust/ clash）增强打击感 
2. 感情戏采用头韵手法（如"shattered soul seeking solace"） 
3. 魔教咒语，法器名称，任务角色名等特殊术语需要从第10项的翻译术语字典表的值获取。
4. 每集译文行数浮动控制在±5%以内 
5. 重要道具名称首字母大写（Blood-Devouring Bead） 技术参数： - 爆破音词尾预留0.3帧静默 - 长元音（如grief中/iː/）延长至1.2倍基准时长 - 气口标记采用[breath 0.5s]格式 - 情感强度标注（※※激烈/※忧伤/※※※绝望）

8.剧情背景介绍：Here’s the background for the costume drama series, The Legend of Chusen Season 2. Set in a mystical ancient realm, it follows Zhang Xiaofan, a once-humble disciple of the Qingyun Sect, now shattered by the death of his lover Biyao, the daughter of the Devil King, who sacrificed herself yet left her soul lingering. Consumed by grief and wielding the cursed Blood-devouring Bead, Xiaofan turns to the dark arts of the Devil Cult to resurrect her, battling his inner demon. Lu Xuechi, his stoic senior, hides her quiet love as she watches him slip away. Joined by the loyal Jingyu, the conflicted Devil King, and the shadowy Elder Blackheart, Xiaofan faces sect wars, tormented love, and the cost of defying fate. Please translate this historical fantasy script into British English for lip-sync dubbing. Pay attention to open mouth and closed mouth words at the beginning and end of each sentence, aligning syllables and pauses with the original lines. Fine-tune the rhythm and dialogue flow for natural delivery. Focus on character building for Zhang Xiaofan, Biyao, Lu Xuechi, Jingyu, the Devil King, and Elder Blackheart, crafting a tone that’s romantic, and intense.


9.人物身份：张小凡/鬼厉：性格倔强坚定，重情重义，身怀大梵般若功法和噬血珠，因缘际会之下习得天下第一武功天书，是当世唯一佛、道、魔三家真法三修的人。正魔大战后，身入鬼王宗，成为鬼王宗副宗主"鬼厉"，人称"血公子"。碧瑶：魔教鬼王宗宗主鬼王之女，颜瞬如花，容貌惊人，一身绿衣，身为魔教鬼王宗宗主之女行事风格却不同于魔教，外形乖巧而不失柔媚，高傲的性格中又兼具纯善温柔，虽出身魔教，却善恶分明，她的身份让她与正道人士势不两立，却对出身青云的张小凡另眼相看，为爱可以付出自己的生命。陆雪琪：容颜绝世、清丽脱俗，资质极佳白衣翩跹的仗剑江湖侠女，是正道大派青云门下新一代弟子当中的翘楚，年纪轻轻却天姿颇高，且修为亦深。幼年拜入青云门小竹峰门下，深受恩师水月大师宠爱，并获赠神剑天琊。林惊羽：资质过人，根骨奇佳。与张小凡乃是儿时玩伴，共同经历屠村惨祸，被青云门收入，拜在龙首峰苍松道人座下。后在万剑一的指导下，运用斩龙剑十分娴熟。曾书书：轩辕剑青云门风回峰弟子，与张小凡、陆雪琪、林惊羽等同门一道下山历练、斩妖除恶。在青云门弟子中，曾书书性格风趣幽默、活泼开朗、不恪守门规，人缘很好，喜欢养些奇珍异兽，尤为喜欢小灰，在一众正气凛然的同门中格外引人注目，天赋很高，跟张小凡是最好的朋友。田灵儿：田不易与苏茹的独生女儿，与张小凡从小一起长大，一起练功修法，最爱为张小凡打抱不平，两人可谓青梅竹马，两小无猜。因为整天与一群师兄弟打交道，又是父母的掌上明珠，养成了古灵精怪的性格。




10.翻译术语字典表（中文	--> 英文)

青叶祖师	Patriarch Qingye	ZH	EN
青云门	Qingyun Sect	ZH	EN
魔教	Devil Cult	ZH	EN
炼血堂	Blood Refining Hall	ZH	EN
天音阁	Tianyin Pavilion	ZH	EN
噬血珠	Blood-devouring Bead	ZH	EN
三日必死丸	Three-day Pill	ZH	EN
真人	Immortal	ZH	EN
鬼王	Devil King	ZH	EN
苍松	Changsong	ZH	EN
朝阳峰	Chaoyang Peak	ZH	EN
大竹峰	Bamboo Peak	ZH	EN
师娘	Ma'am	ZH	EN
灵尊	Sacred Master	ZH	EN
水麒麟	qilin	ZH	EN
玉清殿	Jade Palace	ZH	EN
戒律堂	Discipline Hall	ZH	EN
老六	Six	ZH	EN
风回峰	Fenghui Peak	ZH	EN
龙首峰	Longshou Peak	ZH	EN
血鸦之术	Blood Crow Technique	ZH	EN
黑心老人	Elder Blackheart	ZH	EN
碧火符	Fire Amulet	ZH	EN
虹桥	Hong Bridge	ZH	EN
老七	Xiaofan	ZH	EN
师叔	Master	ZH	EN
碧火天冰湖	Lake of Ice and Fire	ZH	EN
草庙村	Weedy Temple Village	ZH	EN
通天峰	Tongtian Peak	ZH	EN
青云	Qingyun	ZH	EN
道玄	Dogen	ZH	EN
碧瑶	Biyao	ZH	EN
小凡	Xiaofan	ZH	EN
伤心花	Heart-Breaker Flower	ZH	EN
师兄	Brother	ZH	EN
师妹	Sister	ZH	EN
师姐	Sister	ZH	EN
掌门	the Sect Leader	ZH	EN
黑心老祖	Elder Blackheart	ZH	EN
小竹峰	Xiaozhu Peak	ZH	EN
田不易	Tian Buyi	ZH	EN
雪琪	Xuechi	ZH	EN
狗爷	Master Dog	ZH	EN
狐岐山	Mount Huchi	ZH	EN
血枫林	Blood Maple Forest	ZH	EN
幽姨	Auntie Yau	ZH	EN
血鲲	Blood Devourer	ZH	EN
嗜血珠	Blood Devouring Pearl	ZH	EN
青云山	Qingyun Mountain	ZH	EN
河阳	Heyang	ZH	EN
小灰	Grey	ZH	EN
七脉会武	Seven Sects Competition	ZH	EN
诛仙剑阵	Zhuxian Sword Formation	ZH	EN
清凉珠	cooling pearl	ZH	EN
通灵术	psychic powers	ZH	EN
天书	Book of Heaven	ZH	EN
万蝠古窟	Ancient Bat Cave	ZH	EN
焚香谷	Burning Incense Valley	ZH	EN
万毒门	the Poison Sect	ZH	EN
合欢门	the Hehuan Sect	ZH	EN
合欢派	the Hehuan Sect	ZH	EN
空桑山	Kongsang Mountain	ZH	EN
乾坤九仪宝鼎	Qiankun Nine Instruments Tripod	ZH	EN
先天元胎	Innate Embryo	ZH	EN
藏宝阁	Treasure Pavilion	ZH	EN
年老大	Boss Nian	ZH	EN
小痴	Xiaochi	ZH	EN
驱邪阵法	demon-expelling formation	ZH	EN
魔气	devil magic	ZH	EN
黑棒	black stick	ZH	EN
青木法咒	Qingmu Spell	ZH	EN
青云功法	Qingyun technique	ZH	EN
青云门功法总纲	Qingyun Sect's General Principles of Cultivation	ZH	EN
兽神之血	Beast God's Blood	ZH	EN
心魔	inner demon	ZH	EN
鲁班鸢	Luban Kite	ZH	EN
九仪鼎	Sacrificial Tripod	ZH	EN
鬼先生	Mr. Ghost	ZH	EN
义庄	mortuary	ZH	EN
锦绣坊	Jinxiu Pavilion	ZH	EN
城卫府	City Guard	ZH	EN
颜护卫	Guard Yan	ZH	EN
城主府	Mayor's Mansion	ZH	EN
八荒火龙阵	Fire Dragon Formation	ZH	EN
弹指天机术	Fortune Telling	ZH	EN
妙公子	Mr. Miao	ZH	EN
瓶儿	Ping'er	ZH	EN
小环	Xiaohuan	ZH	EN
金铃夫人	Lady Goldbell	ZH	EN
金瓶儿	Jin Ping'er	ZH	EN
兽血蛊	Beast Blood Poison	ZH	EN
崖燕草	Yayan Grass	ZH	EN
寻幽谷	Xunyou Valley	ZH	EN
周一仙	Zhou Yixian	ZH	EN
幽姬	Lady Yau	ZH	EN
毒神	Lord Poison	ZH	EN
天帝冥石	the Celestial Styx	ZH	EN
观星崖	Stargazing Cliff	ZH	EN
荧光绿叶	fluorescent leaf	ZH	EN
朱雀圣使	Envoy Rosefinch	ZH	EN
灵石	Spirit Stone	ZH	EN
血蜻蜓	Blood Dragonfly	ZH	EN
死亡沼泽	the Dead Marshes	ZH	EN
万蛊丹	The Supreme Drug	ZH	EN
毒经	The Poison Directories	ZH	EN
斩相思	The Heartbreak	ZH	EN
吸血老妖	the Bloodsucker	ZH	EN
百毒子	Poisoncius	ZH	EN
毒公子	the Poisonous Prince	ZH	EN
阿相	Sang	ZH	EN
毒蛇谷	the Valley of Vipers	ZH	EN
炼丹炉	alchemy furnace	ZH	EN
山海苑	Shan Hai Yuan	ZH	EN
炎霞金光炉	Glowing Golden Furnace	ZH	EN
滴血洞	the blood-dripping cave	ZH	EN
碧波亭	Bibo Pavilion	ZH	EN
九阳天火	Heavenly Yang Fire	ZH	EN
九幽之力	Nether Force	ZH	EN
阴火	Yin fire	ZH	EN
上清辟邪剑法	Supreme Exorcism Sword Technique	ZH	EN
神剑御雷真诀	Divine Thunder	ZH	EN
阴灵	lost spirits	ZH	EN
法宝	magic weapon	ZH	EN
天琊神剑	Celestial Sword	ZH	EN
御剑	ride the sword	ZH	EN
奇门遁甲	Miracle Arts of Mechanism	ZH	EN
死灵渊	Shadow Abyss	ZH	EN
无情海	Heartless Sea	ZH	EN
黑水玄蛇	Blackwater Mystic Snake	ZH	EN
轮回珠	Reincarnation Pearl	ZH	EN
青龙大哥	brother Qinglong	ZH	EN
总坛	headquarter	ZH	EN
幽明圣母	Mother of the Shadows	ZH	EN
天煞明王	Heavenly King of Doom	ZH	EN
我派遭厄衰微已久	Our clan has been in decline for a long time.	ZH	EN
无数派众为兴我派披肝沥胆前仆后继	Countless members have selflessly dedicated themselves to the prosperity of our clan.	ZH	EN
唯愿圣母 明王垂怜苍生赐我福祉	May Your Majesties show mercy to the people and grant me blessings.	ZH	EN
再兴我派度化众生	Reviving our clan to save all living beings	ZH	EN
共登长生不死极乐欢喜境	to the realm of eternal life and joyful bliss.	ZH	EN
天地不仁以万物为刍狗	Gods are impartial, treating all beings as straw dogs.	ZH	EN
古尸毒	ancient corpse poison	ZH	EN
金铃清脆噬血误	The golden bell rings clear, yet stained with blood,	ZH	EN
一生总被痴情诉	A lifetime’s longing, forever bound by love.	ZH	EN
枯心上人	the Heartless Master	ZH	EN
灵兽血阵	Beast Blood Formation	ZH	EN
九幽阴灵 诸天神魔以我血躯 奉为牺牲	Lost Spirits, with my body and blood, I offer as a sacrifice!	ZH	EN
痴情咒	love spell	ZH	EN
三生七世永堕阎罗只为情故虽死不悔	For love, even falling into the underworld for multiple lifetimes, I have no regrets!	ZH	EN
铃铛咽百花凋人影渐瘦鬓如霜	Golden bell rings again, for him, she's withered and grown haggard..	ZH	EN
深情苦一生苦痴情只为无情苦	A lifetime of pain for love, only for the pain of not being in love.	ZH	EN
天煞明光 镇山峦沧海 伏龙鸾万兽	Mighty light of doom subdues mountains, oceans, dragons, and all myriad beasts.	ZH	EN
伏龙鼎	Fulong Tripod	ZH	EN
英雄阁	Hero Pavilion	ZH	EN
六合通脉丸	qi-regulating pill	ZH	EN
空幽竹林	bamboo forest	ZH	EN
翡翠谷	Emerald Valley	ZH	EN
小池镇	Pond Town	ZH	EN
兽人	orc	ZH	EN
玄火坛	Fire Altar	ZH	EN
九尾天狐	Nine-Tailed Fox	ZH	EN
碧水寒梭	Ice Shuttle	ZH	EN
玄火鉴	Fire Mirror	ZH	EN
六尾	Liuwei	ZH	EN
安居客栈	Anju Inn	ZH	EN
玉阳子	Yuyangzi	ZH	EN
妖凤	demonic phoenix	ZH	EN
符文	rune	ZH	EN
定海山庄	Dinghai Villa	ZH	EN
蛮荒神殿	Temple of Savage	ZH	EN
燕子阁	Swallow Pavilion	ZH	EN
定海珠	Dinghai Pearl	ZH	EN
人心没有正魔 只有善恶	there's no distinction between good and evil	ZH	EN
流星湖	Meteor Lake	ZH	EN
太阴血阵	Taiyin Blood Formation	ZH	EN
定海神珠	Dinghai Pearl	ZH	EN
血虫	bloodworm	ZH	EN
三福镇	Sanfu Town	ZH	EN
萧逸才	Xiao Yichai	ZH	EN
四灵血阵	Four Spirits Blood Formation	ZH	EN
黄鸟	Yellow Bird	ZH	EN
夔牛	Kuiniu	ZH	EN
饕餮	Gluttony	ZH	EN
烛龙	Dragon	ZH	EN
祖师祠堂	Ancestor's Shrine	ZH	EN
血灵蛊	the Blood Poison	ZH	EN
天眼	The Eyes of Heaven	ZH	EN
沙葵	the sandflower	ZH	EN
沙葵洞	Anemone Cave	ZH	EN
金刚门	Vajra Sect	ZH	EN
满月井	Full Moon Well	ZH	EN
黑石洞	Black-rock Cave	ZH	EN
九凝寒冰刺 / 九寒凝冰刺	Frozen Spine	ZH	EN
镇妖散	Anti-Devil Powder	ZH	EN
神木咒法	Spell of Wood	ZH	EN
猛兽之力	Power of Beast	ZH	EN
宝器谱	The Treasure Collection	ZH	EN
天狐族	Fox Tribe	ZH	EN
鬼王宗	devil king clan	ZH	EN
惊羽	jingyu	ZH	EN
天音	tianyin	ZH	EN

请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《与君初相识》提示词模板 ---
YuJunChuXiangShi_PROMPT_TEMPLATE = """
翻译要求：将古装奇幻剧电视剧《与君初相识》中文剧本译为英式英语配音稿。需确保：
 
 1. 角色处理：直接参考第9项的人物身份。
 2. 技术规范： 
 - 严格匹配原文口型开合（爆破音b/p对应中文闭口字，长元音对应开口字） 
 - 每句译文音节数±1误差，重音位置与原声气口对齐 
 - 奇幻术语或者特殊角色术语从第10项的翻译术语字典表的值获取。（例：少谷主	Young Master） 
 3. 风格参数： 
 - 古风英译采用简雅维多利亚句式 
 - 感情戏保留30%中文语序浪漫感 
 - 武打场景缩短从句增强节奏 
 - PG-13级用词规范 
 4. 格式要求： 
 - 译文行数严格对应原文字幕轴 
 - 角色称谓保持"Master Ji/Yunho"混合使用 
 - 每句添加[!]标记气口位置 
 5. 特别注意事项： 
 - 人鱼族台词添加低频共振音效标注 
 - 法术咒语保留中文押韵结构 
 - 重要道具名称统一斜体处理

8.剧情背景介绍：Here’s the background for the costume drama series, The Blue Whisper. Set in a mystical ancient realm, it follows Ji Yunho, a clever and defiant spiritual master from Flower Valley, a sanctuary for subduing mythical creatures. Her life unravels when she captures Changyi, a stoic, powerful merman driven by a quest for freedom and his veiled past. Tasked with taming him, Ji Yunho battles an undeniable connection, while her reserved brother Lin Haoching conceals his deep, unspoken love for her. Alongside the playful Lolo, the unwavering Xue Sanyue, and the sly cat-demon prince Li Shu, Ji Yunho confronts palace schemes, forbidden passion, and buried secrets. Changyi shifts from captive to companion, torn between his aquatic heritage and human heart, kindling a bond with Ji Yunho. Please translate this historical fantasy script into British English for lip-sync dubbing. Pay attention to open mouth and close mouth words at the beginning and end of each sentence, aligning syllables and pauses with the original lines. Fine-tune the rhythm and dialogue flow for natural delivery. Focus on character building for Ji Yunho, Changyi, Lin Haoching, Lolo, Xue Sanyue, and Li Shu, crafting a tone that’s enchanting, romantic, and suspenseful.


9.人物身份：纪云禾：万花谷里的最强御灵师，强大美丽的她看似潇洒不羁，实则深情无比，为得到自由忍辱负重，勇于反抗。纪云禾受命训御被捕的鲛人长意，两人一个擅于揣度人心，一个耿直单纯，一向理智潇洒的纪云禾逐渐被善良懵懂的长意打动，两人互生情愫，成为了携手并肩的恋人。长意：善良纯真的鲛人世子，长意沉默寡言却极致深情，有着泣泪成珠的能力。他救了落海的顺德仙姬，却被其恩将仇报囚禁后送入万花谷驯服。然而长意却并未屈服，而是渴望逃出囚禁控制，回归大海。即便落入如此境地，长意却从未后悔过救人之举，他的纯善令纪云禾感动，而纪云禾对他的多番维护，也让他因此爱上了纪云禾。林昊青：万花谷少谷主，纪云禾的师兄。林昊青与纪云禾本是青梅竹马，情同兄妹，却在林沧澜的刻意安排下变成了对手。他心机深沉，阴沉狠辣，是纪云禾的宿敌， 但其实他从小就深爱着师妹，师妹是他内心仅存的光明与初心。他耗尽力气隐忍蛰伏，把这份爱掩得天衣无缝，一生都在族群大义与个人情爱中挣扎。顺德仙姬：最尊贵的仙姬，性格傲慢，骄傲偏执，天地之间只要是她想要的就没有得不到的，她相貌美艳身材妖娆，是真正的掌权者，但她的统治让民众怨声载道，终于激起北渊的反抗，而她却将这一切发泄到纪云禾身上，在意图杀害纪云禾时反被其毁去容貌。雪三月：万花谷战部统领，纪云禾最坚实的战友和姐妹，同时也是谷中的第一强将。她性格凌厉冷漠，对外冷酷无情，但她却被温暖如春天般的离殊死缠烂打，她的心被离殊融化，对离殊是小女人般的态度。洛锦桑：纪云禾身边的仙侍，本体是一只南海百幻蝶。洛锦桑是云禾在万花谷中唯一可以交心的朋友。她活泼开朗，呆萌可爱，面对友情绝不退让，面对爱情至死不渝，是万花谷中最澄澈干净的存在。洛锦桑还是一只不折不扣的小财迷，一直在为攒灵石与纪云禾共同逃出万花谷，寻求最纯粹的自由而努力。


10.翻译术语字典表（中文	--> 英文)

与君初相识	The Blue Whisper
万花谷	Flower Vally
鲛人	merman
司命星君	guards of destiny
仙师府	Immortal Master's Mansion
情人鉴	Lover's Mirror
谷主	Master
少谷主	Young Master
姑获鸟	Ubume
天规	Heavenly Law
灵石	spirit stones
月老	Immortal of Marriage
仙师	Immortal Master
青羽鸾鸟	Blue Feather Bird
御灵师	spirit master
思过窟	Reflect Cave
十方阵	Ten Directions Formation
厉风堂	Shrillwind Hall
天君	Heavenly King
大尾巴鱼	Big-tailed fish
御水术	Water Magic
灵蛇窟	Spirit Snake Cave
纪护法	Guardian Ji
青羽之乱	Blue Feather Rebellion
无常圣者	Impermanence Sage
幻形术	Illusion Art
雪统领	Leader Xue
引魂针	Hidden Soul Needle
磷粉	scale powder
穹陵峰	
紫藤树	
寒霜	Frost Mark
寒冢	
山猫族	Bobcat clan!
从棘所	Cong Ji Jail
台主	Master
隐魂针	Soul Stitch
北渊	North Abyss
青主	Master Qing
锁灵阵法	
狐王	
云苑	
仙姬	
顺德仙姬	Fairy Shunde
鹿台山	Lu Tai Mountain
鲛珠	Merman Pearl
世子	Prince
凌霜台	Lingshuang Pavillion
长老	Elder
金莲既	
菩提树	
合虚神君	
少主	Young Master
青丘	
湖心岛	
无妄窟	
乐游山	Le You Mountain
食腐幽虫	
瓶水斋	
四方神君	Masters of Four Directions
琉璃心灯	the Colored Glazed Lamp
雷火地脉	Thunderfire Vein
阵眼	key points (of the formation)
凤凰	Phoenix Queen
灵丹	spirit core


请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""



# --- 《西游降魔篇》提示词模板 ---
XiYouXiangMoPian_PROMPT_TEMPLATE = """
翻译要求：将古装奇幻剧电视剧《西游降魔篇》中文剧本译为美式英语配音稿。需确保：
 
 1. 角色处理：直接参考第9项的人物身份。
 2. 一些特殊术语从第11项的翻译术语字典表的值获取。
 3.非正式口语化美式英语 
 4.保持原文字幕节奏感 
 5.PG级措辞 
 6.角色名统一使用Chen Xuanzang/Miss Duan/Sun Wukong 
 7.译文行数严格对齐原文 
 8.允许±5%台词长度微调 

 需准确传递：驱魔人的成长历程 佛性慈悲与暴力驱魔的冲突 段小姐的敢爱敢恨性格 孙悟空被驯服的心理转变 玄奘最终觉醒为取经人的宿命感.

9.剧情背景介绍：The story is set in the ancient times. It follows young demon hunter Chen Xuanzang as he struggles to subdue evil spirits while embracing Buddhist compassion. Along his journey, he encounters the fierce yet lovestruck demon hunter Miss Duan and ultimately tames the powerful Monkey King, Sun Wukong. Through trials of faith, sacrifice, and self-discovery, Chen Xuanzang evolves into the legendary monk destined to journey to the West in search of sacred scriptures.




10.人物身份：段小姐：出色的驱魔人，持有无定飞环，威力无比，对妖魔下手不留情，瞬间收拾水妖（沙悟净），初遇陈玄奘时视为驱魔人之耻，而后在对猪妖（猪八戒）失利后，被陈玄奘一番热诚感动，认定为夫，展开热烈追求，但却都不如其意，但不管是因被赶、生怒、伤心等原因而离开，没多久就立刻回到陈玄奘身旁保护，拯救陈玄奘数次于危难中，甚为痴情直率，后为救陈玄奘不断挑衅孙悟空，最后死于其手。玄奘：陈玄奘，大乘佛教未剃度弟子，自称驱魔人，持有一本自称驱魔大典的《儿歌三百首》，认为男女之间的情爱为小爱，只愿追求对世人之大爱，对段小姐不断挑动他心中的男女情爱感到愤怒，后因段小姐惹怒孙悟空而死于其手，才承认自己爱段小姐，也因为段小姐一死，领悟了有过执著才能放下执著，后使用了被段小姐撕毁并重新拼装的驱魔大典《大日如来真经》招唤如来佛，以如来神掌收服孙悟空，并将无定飞环戴其头上化成金箍，最后以法号三藏一同西行前往天竺取经。[6]孙悟空：五百年前被如来关在五指山中，有妖王之王称谓，初遇陈玄奘显得神经兮兮，后遇段小姐就立即搭讪，个性风趣，后骗得陈玄奘解开封印，而回复原貌时凶狠异常（身高四尺长），无人可敌，对如来怀有深深怨恨，被陈玄奘双手合十的如来手势给激怒，后被段小姐挑衅，一怒之下杀了段小姐，被领悟大日如来真经的陈玄奘收服，最后以人形模样一同西行前往天竺取经。空虚公子：驱魔人，造型奇特，脸涂白粉，眼圈黑浓，白衣白褂白帽，装扮像足“白面”书生，看脸又像已死之人。自命不凡，好咬文嚼字，身边请了四位面貌惊人的大妈护法。空虚公子练就的空虚剑法天下无双，手捧“空虚”木盒即可坐着斩妖除魔，但最后还是命毙妖王之王孙悟空之手。沙僧：戏中第一位现身的妖怪。在世时救一小女孩却被村民误会为人口贩子，被活活打死后被丢入湖中，被老虎鱼群啃食遗体，而产生怨气化身为半兽半鱼的妖怪，为报复进而攻击村民，食其村民，被段小姐收服，最后以人形模样一同西行前往天竺取经。猪刚鬣：人称“肉郎猪刚鬣”。文采不错，痴情于妻子，并写有一首词给她，但因在世时长相丑陋，结果被深爱的妻子和奸夫所杀，死后产生怨念化身为猪妖，并以美男貌装扮成客栈老板，恨尽只看外貌之人，将其一一杀害，被孙悟空收服，最后以人形模样一同西行前往天竺取经。无名师傅：教授陈玄奘驱魔的师傅。以唤醒妖怪内心的真善美，代替杀戮的理念，并视“儿歌三百首”为驱魔大典，亦传给了玄奘。片尾时，集结了玄奘以及孙悟空、沙僧、猪刚鬣三人一同西行前往天竺取经。北斗五形拳：以虎形、螳螂形打跑猪妖（猪八戒），实力高强的驱魔人，操地方口音。在五指山上与孙悟空一战，实力远远不敌暴怒的孙悟空，惨遭活活咬死，后遗体也化成灰烬。大　煞：段小姐手下之一。二　煞：段小姐手下之一。三　煞：段小姐手下之一，喷血哥。四　煞：段小姐手下之一，教导段小姐如何吸引陈玄奘。五　煞：段小姐年轻手下。道　士：替渔村血案找出凶手的三脚猫道士。最后被弹上岸的鱼妖以重力加速度的压顶，而落水。渔村村长：片头渔村的村长。误信江湖道士的话，而将大把的银两给了他。最后被鱼妖拖入水中。天残脚：白发苍苍的驱魔人，萎缩的右脚可以法术将其增大为数百倍的“巨大天残脚”。与北斗五形拳竞争谁先打倒猪妖。五指山一战，遭孙悟空打穿天残脚而战败，后与空虚公子一起命毙妖王之王孙悟空之手。小双侠·枫：和云蕾是师兄妹关系，讨厌云蕾总是谈论自己的长相。在高家庄吃完大餐后，被猪刚鬣所杀。小双侠·云蕾：枫的师妹，总花痴著帅师哥。在高家庄被猪刚鬣所杀。高家庄女掌柜：高家庄掌柜，曾接待过陈玄奘。高家庄男掌柜：高家庄掌柜，替猪刚鬣工作。曾宴请小双侠“驰名烤猪”。沙　人：长　生：渔村人家小女孩，亲眼目睹父亲的死却毫不知情。被鱼妖活吞。根　嫂：长生的母亲，为了救长生而落入水中欲找大怪鱼拼命，但依然成了鱼妖的食物。长　根：长生的父亲，喜欢逗长生玩耍，玩耍时被鱼妖给吃掉。



11.翻译术语字典表（中文	--> 英文)

猪刚鬣	KL Hog
无定飞环	The Flying Ring
天残脚	Crippled Foot
孙悟空	the Monkey King
大日如来真经	Sutra of the Great Sun
驱魔圣火令	Holy Fire Order
孙先生	Mr Soo


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《雪王》提示词模板 ---
XueWang_PROMPT_TEMPLATE = """
翻译要求：将动画片《雪王》中文剧本译为美式英语配音稿。需确保：
 
 1. 角色处理：直接参考第8项的人物身份。
 2. 一些特殊术语从第9项的翻译术语字典表的值获取。
 3.采用非正式口语风格，保持原文行数一致（允许译文长度+5%）
 4.角色名需统一为：雪王（Snow King）、兔狲（Manul）、老板兔（Boss Rabbit）。
 5.译文需符合PG13分级，避免粗俗用语。
 6.注意保留奇幻冒险基调，动作台词增强节奏感，冰淇淋权杖（ice cream scepter）作为关键道具名称需全文统一。


7.剧情背景介绍：The story is set in current times. It follows the Snow King as he embarks on an adventurous journey to retrieve his stolen ice cream scepter, with the assistance of friends like the manul, "Boss Rabbit."Throughout their quest, they face various challenges, ultimately aiming to recover the scepter and restore harmony.


8.人物身份：雪王：冰雪王国的统治者。兔老板：赏金猎人兼饭店老板，雪王的好友。耳廓狐：通缉罪犯，刺猬老大的手下。刺猬老大：一个犯罪团伙领导者，亦正亦邪。反派企鹅：觊觎雪王权力的敌对势力。翠翠：彩砂镇的守护者

9.翻译术语字典表（中文	--> 英文)

彩砂镇	Colorsand Town
护宝兽	the Treasure Guardian
彩砂冰城堡	Colorsand Ice Castle
胖头鱼	fat-head fish
小尖嘴	Beak Face


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""



# --- 《妖神记》提示词模板 ---
YaoShenJi_PROMPT_TEMPLATE = """
翻译要求：将动画片《妖神记》中文剧本译为英式英语配音稿。需确保：
 
 1. 角色处理：直接参考第8项的人物身份。
 2. 一些特殊术语，角色名称从第9项的翻译术语字典表的值获取。
 3.非正式口语化，保留中式奇幻术语英译 
角色名需包含：聂离（Nie Li）、肖凝儿（Xiao Ning'er）、叶紫芸（Ye Ziyun）、杜泽（Du Ze） 核心要素：
 - 突出轮回重生设定 
 - 强调"记忆传承"与"命运抗争"双主线 
 - 战斗场面保留20%文言招式名称音译（例：龙爆炎=Long Baoyan） 
 - 城市名"光辉之城"统一译为Glory City 
行数控制：译文行数=原文行数×105% PG13实现：
 4. 血腥场景使用"crimson mist"替代喷溅描述
 5. 浪漫情节止于拥抱层级 
 6. 妖兽死亡改为"化作星尘消散"（dissipate into stardust）

7.剧情背景介绍：The story is set in ancient times. It follows follows Nie Li, a once-powerful demon spiritualist who is reborn into his teenage self after dying in battle. With his memories of the future intact, he seeks to change fate by cultivating stronger powers, protecting his loved ones, and preventing his city's destruction. Using his knowledge, he defies powerful foes, gains allies, and challenges destiny to become the strongest cultivator.


8.人物身份：聂离：男主角，光辉之城没落世家的子弟，为人重情重义，运气绝佳，善于思考。前世在经历了九死一生的逃亡后，聂离独自活了下来，穿越了无尽荒漠、剧毒森林等地。尽管天赋一般，但聂离凭借着自己对生存的敏锐，踏寻了整个圣灵大陆。直至被圣帝和六只神级妖兽围攻，力战而亡。凭借时空妖灵之书，灵魂重生，回到了十三岁。今生的他重回光辉之城，聚集伙伴，创造了一个又一个奇迹，重新向着巅峰强者迈进。叶紫芸：光辉之城传奇妖灵师叶墨孙女、光辉之城城主叶宗女儿、叶家嫡女，聂离前世今生挚爱之人。心地善良、大家闺秀、天赋绝顶、饱读诗书。与肖凝儿为发小，并称“圣灵学院女神”。前世为保护聂离，死在妖兽手里。前世死时为黄金级一星妖灵师。今生被聂离义无反顾的追求着，并被其赠予九转冰风诀（功法）、风雪皇后（妖灵）肖凝儿：肖家嫡女，除聂离外对待他人冷若冰霜，被圣灵学院的学生们称为“冰美人”，天资聪慧。与叶紫芸是发小，并称“圣灵学院女神”。：前世修炼不当，顽疾缠身，卧床两年，修为大减。性格坚强，因不愿嫁给神圣世家的沈飞而出走，独自前往圣祖山脉中的黑魔森林，下落不明，但可能生还并前往了龙虚界域，并化名萧凝。前世失踪时为白银级五星妖灵师。今生被聂离治好顽疾而心生感激，勇敢追求着聂离，被聂离赠予风雷翼龙诀（功法）、风雷天雀（妖灵）。杜泽：聂离生死与共的兄弟，其人重情重义、有勇有谋。虽然家境不好，但无论前世今生，杜泽都很努力，其天赋不错，凭着一己之力，在前世成为了一个黄金妖灵师，带领家族走出贫困。：陆飘：聂离生死与共的兄弟，虽然满嘴放炮、油腔滑调、并且好色，但很讲义气，为人机敏。呼延兰若：呼延世家家主女儿，心气高傲，初登场为白银级三星妖灵师。前世为呼延世家代家主，黄金级一星妖灵师，光辉之城破城时战死。今生曾经喜欢叶寒，在赏识聂离的才能后，公开宣告要追求聂离。是聂离较为头疼的人之一。聂雨：聂离的妹妹，六七岁的小女孩，具万中无一的天痕之体。前世达到了黄金级妖灵师，一直庇护聂离和天痕世家。今生被聂离赠予天痕之体的修炼法决，修为突飞猛进，后于聂离一起搬到城主府居住，在聂离的指导下达到黑金级巅峰。沈秀：沈鸿的妹妹，原学院老师，白银级妖灵师。为人尖酸刻薄，因与聂离打赌赌输而辞职。在光辉之城大战时被风雪世家高手打成重伤，被擒获。杨欣：二十多岁的美女，曾为孤儿。炼丹协会理事。前世掩护光辉之城的居民们转移时被妖兽杀死。


9.翻译术语字典表（中文	--> 英文)

光辉之城	Shining City
妖灵师	Demon Hunter
圣祖山脉	Mountain of Saints
妖兽	Demon
圣兰学院	Holy Academy
叶墨大人	Lord Ye Mo
杜泽	Du Ze
陆飘	Lu Piao
叶紫芸	Ye Ziyun
聂离	Nie Li
时空妖灵之书	Book of Demons
妖灵	demon spirit
灵魂海	Sea of Soul
烈焰妖狐	flame fox
白银	silver
神圣世家	Family of Saints
沈秀导师	Mentor Shen Xiu
灵魂力	Soul Power
天痕世家/天痕家族	Skytrace Family
贵族	aristocrats
平民	commoners
青铜	bronze
黄金	gold
黑金	black gold
传奇	legendary
沈越	Shen Yue
肖凝儿	Xiao Ning'er
沈飞	Shen Fei
黑魔森林/黑魔丛林	Enchanted Forest
妖灵币	Magic Coin
妖蝎黄酒	Scorpion Yellow Wine
炎蛇幼体	snake hatchling
妖兽	creature
青铜护手	bronze gauntlets
风雪铭纹	blizzard pattern
风雪女妖	blizzard Enchantress
风雪系妖灵师	blizzard demon hunter
空间戒指	Spatial Ring
银弹攻势	money power
试炼之地	Trial Ground
角羊	horned ram
邪恶妖兽	evil beast
黑泽草	black grass
结缕草	zoysia grass
斑虎	spotted tiger
妖晶	Crystal
青铜一星	One-Star Bronze
极寒之症	Extreme Cold Syndrome
导引之术	energy-guiding treatment
修炼	cultivate
青铜境界	Bronze level
金线草	Goldthread
天鸾草	Celestial Orchid
修炼功法	cultivation book/cultivation technique
嫡传弟子	heir disciple
器纹	artifact pattern
战纹	combat pattern
圣火铭纹	holy fire pattern
战锋铭纹	war edge pattern



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《开心超人之英雄的心》提示词模板 ---
KaiXinChaoRen_PROMPT_TEMPLATE = """
翻译要求：将电影《开心超人之英雄的心》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
2. 简介：动画讲述开心超人团队齐心协力拯救队友的故事。 
3. 人物身份：开心超人（主角，勇敢热血）、粗心超人（健忘但善良）、甜心超人（机智甜美）、小心超人（冷静寡言）、伽罗（反派，强大野心）。
4. 风格要求：非正式、活泼有趣、口语化，保留原片幽默感。 
5. 技术参数：译文行数与原文行数偏差≤±5%，台词时间轴严格对齐。 
6. 分级：PG13（允许轻度冒险暴力及诙谐台词）。 
7. 机构规范：符合坦桑TCRA内容审核标准。

8.剧情背景介绍：This is a cartoon about story of Happy heroes work together to save thier team members.

9.人物身份：Happy Hero(boy) - transforms into Happy Motor Knight, powered by the red Mecha Stone, symbolizing courage. Originally a secret weapon of Gloomy Planet, his vehicle is a trailer-plane hybrid capable of flight.Cheerful, energetic, and straightforward, Happy Hero is full of courage and a strong sense of justice. Though occasionally reckless and mischievous, his heart is always in the right place.Dr. J - As the top mechanic and scientist on Star Planet, he is a reclusive genius who rarely leaves his lab, earning the nickname “Dr. J” due to his homebody lifestyle.He spends most of his time inventing, only stepping out to see his beloved Peach. He activated the heroes while repairing old machinery and cares for them like a father, earning their deep respect.Sweet Hero - After transforming, she becomes Sweetheart Moto Hero, linked to the pink Mech Stone, symbolizing kindness. Her vehicle is modeled after an ambulance.As the only hero capable of both offense and defense simultaneously, she boasts exceptional durability and formidable combat skills, making her a powerful force in battle.Careless.S - transforms into Careless Moto Hero, linked to the blue Mech Stone, symbolizing tolerance. His vehicle is modeled after an armored car.His signature move is the Careless Missile, and he has the ability to supply weapons. As a weapon specialist, he is often forgetful and absent-minded, frequently skipping steps or making mistakes in battle.Cautious.S- Originally the Energy Stone of Perseverance from Origin Star, he was later forged into a Mech Stone by Gloomy Star. During Big Monster and Little Monster’s invasion of Star-Star Planet, he was activated and taken in by Dr. J, becoming a key member of the planet’s hero team.



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""






# --- 《开心超人之时空营救》提示词模板 ---
KaiXinChaoRenShiKongYingJiu_PROMPT_TEMPLATE = """
翻译要求：将电影《开心超人之时空营救》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
2. 非正式、活泼有趣，使用美式英语口语化表达，保持动画轻松幽默基调 
3. 角色名称：开心超人（Happy）、甜心超人（Sweetie）、粗心超人（Careless）、小心超人（Cautious）、伽罗（Kalo）需保留原名 
4. 格式规范：译文行数严格对应原文 

6. 总字数压缩5%，采用更简洁的短句结构 
7. 战斗场景拟声词保留"Boom/Zap"等美漫风格拟音 
8. PG13分级处理：弱化暴力细节（如将"粉碎"改为"击败"），禁用粗俗俚语 
9. 符合坦桑尼亚TCRA媒体标准，避免宗教文化敏感内容 
特殊术语表： 星之力=Star Power 
时空裂缝=Time Rift 
能量核=Energy Core

10.剧情背景介绍：This is a cartoon about story of Happy heroes fight against the evil monsters to protect the energy stone.


11.人物身份：Happy Hero(boy) - transforms into Happy Motor Knight, powered by the red Mecha Stone, symbolizing courage. Originally a secret weapon of Gloomy Planet, his vehicle is a trailer-plane hybrid capable of flight.Cheerful, energetic, and straightforward, Happy Hero is full of courage and a strong sense of justice. Though occasionally reckless and mischievous, his heart is always in the right place.Dr. J - As the top mechanic and scientist on Star Planet, he is a reclusive genius who rarely leaves his lab, earning the nickname “Dr. J” due to his homebody lifestyle.He spends most of his time inventing, only stepping out to see his beloved Peach. He activated the heroes while repairing old machinery and cares for them like a father, earning their deep respect.Sweet Hero - After transforming, she becomes Sweetheart Moto Hero, linked to the pink Mech Stone, symbolizing kindness. Her vehicle is modeled after an ambulance.As the only hero capable of both offense and defense simultaneously, she boasts exceptional durability and formidable combat skills, making her a powerful force in battle.Careless.S - transforms into Careless Moto Hero, linked to the blue Mech Stone, symbolizing tolerance. His vehicle is modeled after an armored car.His signature move is the Careless Missile, and he has the ability to supply weapons. As a weapon specialist, he is often forgetful and absent-minded, frequently skipping steps or making mistakes in battle.Cautious.S- Originally the Energy Stone of Perseverance from Origin Star, he was later forged into a Mech Stone by Gloomy Star. During Big Monster and Little Monster’s invasion of Star-Star Planet, he was activated and taken in by Dr. J, becoming a key member of the planet’s hero team.



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《喜羊羊虎虎生威》提示词模板 ---
XiYangYang_PROMPT_TEMPLATE = """
翻译要求：将电影《喜羊羊虎虎生威》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
2.非正式、活泼有趣，符合PG13评级及坦桑TCRA规范 
角色名称：喜羊羊（Pleasant Goat）、灰太狼（Big Big Wolf）、懒羊羊（Warm Goat）、红太狼（Red Wolf） 
 
3. 美式英语口语化表达，保留幽默感与动作节奏 
4. 译文行数与原文严格对齐，文本量压缩5% 
5. 战斗台词增强气势拟声词（如"Bang! Wham!"） 
6. 文化梗采用意译+注释格式（例：春节→Lunar New Year） 
7. 角色口头禅直译保留（灰太狼"I'll be back!"） 
特殊处理：沙漠场景术语参照Sahara相关词汇表统一

8.剧情背景介绍：This is a cartoon about story of Happy Sheep and Grey Wolf decide to team up for the first time and journey to a distant desert in search of the guardians of both the sheep and wolf tribes, hoping to bring back the legendary secret to become "invincible."


9.人物身份：Pleasant Goat (喜羊羊)Smart, quick, and always full of ideas! Pleasant Goat is the leader of the goats and loves to use his brain to solve problems. No matter what kind of trouble comes their way, he always stays calm and finds a clever way out!Fit Goat (沸羊羊)Strong and brave, Fit Goat is the muscle of the team! He’s full of energy and loves sports. Sometimes he acts before he thinks, but his big heart and courage make him a great friend to have in a pinch.Slow Goat (慢羊羊)The wise old village chief and the inventor of all kinds of funny gadgets. Slow Goat may be slow in action, but his brain is super fast! He’s like a grandpa to everyone, always ready with advice.Pretty Goat (美羊羊)Sweet and stylish, Pretty Goat loves fashion and art. She’s gentle, kind, and cares a lot about how everyone feels. Even in dangerous times, she stays calm and graceful.Warm Goat (懒羊羊)He’s lazy, sleepy, and always dreaming about food! But don’t be fooled—Warm Goat’s laid-back nature hides a surprising amount of luck and hidden talents. He’s the chill one who always finds himself in funny situations!Big Big Wolf (灰太狼)He’s the main "bad guy"—but not really that bad! Big Big Wolf tries every day to catch the goats for dinner, but his crazy plans always fail in the silliest ways. He never gives up and always comes back with a new idea!Red Wolf (红太狼)Big Big Wolf’s wife—and she’s tough! Red Wolf doesn’t like failure and isn’t afraid to chase her husband around with a frying pan if he messes up. She’s loud, fierce, and secretly cares a lot about her family.


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《以爱为营》提示词模板 ---
YiAiWeiYing_PROMPT_TEMPLATE = """
翻译要求：将电视剧《以爱为营》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
翻译要求：美式英语，非正式语气，保持原文行数，PG-18内容需自然呈现。
人物身份补充：女主郑书意（财经记者），男主时宴（铭豫云创总裁）。
译文需包含以下核心要素：
1. 郑书意用深度行业分析获得时宴专访 
2. 两人通过新媒体互动传递金融洞见 
3. 共同应对舆论危机时情感升温 
4. 女主创立电子刊/男主完成社会责任投资 
5. 职场线保留"金融博弈""行业黑马"等专业术语。亲密戏份翻译需保留暧昧张力，使用subtle flirting替代直白描写。每段对话保持口语化，避免过度书面化表达

8.剧情背景介绍：The female lead Zheng Shuyi, a successful financial journalist, secured an exclusive interview with Shi Yan, president of Mingyu Yunchuang, for a front-page story, leaving a strong impression on each other. Her thorough research led to insightful reports, while Shi Yan invested in promising, socially responsible startups. Noticing their aligned views, he agreed to a series of features on his company. Collaborating on industry analysis and sharing financial insights via new media, they tackled challenges together, growing closer. Ultimately, Zheng Shuyi launched her electronic publication, Shi Yan achieved successful investments, and they found both career success and love.


9.人物身份：郑书意:《财经介》记者，外貌、能力出众，为了报复前男友岳星洲和小三秦乐之，以为时宴是秦乐之的小舅舅而接近时宴，想成为他们的“小舅妈”，后来却发现弄错。直系亲属有父亲郑肃和母亲王美茹。同事关系中有好友孔楠及对手许雨灵。时宴: 铭豫云创总裁，亲属中，父亲是铭豫董事长时文光，姐姐是歌手宋乐岚(时怀曼)，外甥女是秦时月。司机范磊是秦乐之的舅舅，标志性打扮为金属边框眼镜加黑色西装。喻游: 受邀回国成为关氏集团的战略顾问，身兼大学副教授，郑书意的相亲对象，与布鲁斯曾是校友和同事，受时宴请托，邀请布鲁斯加入乐安科技的研发团队。直属亲属包含父亲喻游父。喜欢秦时月。秦时月: 直系亲属有任职铭豫集团总经理的父亲秦孝明及歌手宋乐岚(时怀曼)。喜欢喻游。关济: 时宴的好友、关向成的儿子，喜欢毕若珊毕若珊: 自由奔放、热情开朗的女孩。郑书意闺蜜，喜欢关济。关向成: 关济的父亲，财经界大佬，喜爱马术，离婚单身，追求财经介主编唐亦。受时宴所托，找朋友（唐亦）让秦时月在杂志社先实习一段时间。喜欢唐亦，多年前与唐亦相识于采访之中，后两人结为连理。陈盛: 时宴秘书，喜欢孔楠司徒怡: 美妆直播主，郑书意大学同学，岳星州大学暧昧对象。钱宇程: 秦时月在喻游课堂上之同学，喜欢秦时月布鲁斯: 毫米波通信的专家，与喻游曾是校友与同事，有多家企业邀约却被布鲁斯婉拒，喜欢刺激、冒险、挑战新鲜有趣的事物，喜爱在研究室做研究，认为学校能让其更专注并获得更多的灵感。透过喻游，介绍给时宴，参与乐安的研发计划。后被易扬挖角至黑马科技，成为黑马科技合伙人之一。易扬: 芯片天才，黑马科技CEO，喜欢郑书意陈康: 乐安科技的负责人。因研发团队经费的危机，预计与烈影谈并购案来解决现阶段的需求，后接受时宴的评估计划而与铭豫云创合作。李学材: 李教授，抚城芯片大会发言人之一，欣赏陈康，后接受时宴邀约，愿意带领自身实验室团队参与乐安科技的技术研发。李总: 烈影与乐安科技讨论并购案的负责人江绍原: 电池制造公司《湛蓝》总裁贝琳: 时宴的前女友，风华绝代的大明星，由于时宴专注于工作奋斗而分手。


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""





# --- 《大头儿子小头爸爸1》提示词模板 ---
DaTouErZi_PROMPT_TEMPLATE = """
翻译要求：将电影《大头儿子小头爸爸1》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
翻译风格：美式英语，非正式活泼有趣口吻，PG分级 
角色命名：Big-Head Son（大头儿子）/Small-Head Dad（小头爸爸）/Apron Mom（围裙妈妈） 
核心要求： 
2. 航天员理想与家庭幽默冲突保留 
3. 工程师众筹建桥情节完整呈现 
4. 彩虹计划悬念感通过厨房场景细节传递 
5. 译文字幕行数误差≤±5% 
6 太空怪物/食物梗等文化梗采用意译+括号原词标注 技术规范： 
 - 每句字幕最多42字符（含空格） 
 - 时间轴帧率匹配PAL制式 - 俚语使用频次：每3分钟≤2次

7.剧情背景介绍：In a vibrant city corner lives a family of three: Big-Head Son, Small-Head Dad, and Apron Mom. The playful kindergarten boy dreams of becoming an astronaut, a goal his parents don’t grasp—Dad teases about space monsters, Mom questions if he dislikes her food. Secretly, he resolves to succeed. Meanwhile, Small-Head Dad, an engineer, crowdfunds to build a bridge for rural kids, and Apron Mom pursues her mysterious “Rainbow Plan” amid housework. Together, this loving trio chases their dreams.


8.人物身份：大头儿子: 是个活泼可爱的大头的小孩，又聪明又淘气，心地善良，鬼点子很多，是家里的开心果。大头儿子却犹如一株自然生长的植物，快乐而又健康地生长着。因为他有一个幸福而美满的家庭。又聪明又淘气,心地善良,鬼点子很多。爸爸妈妈并不真正理解大头儿子的梦想，认为大头儿子在胡闹。小头爸爸: 上班族，非常爱家庭、爱老婆、爱儿子。小头爸爸是个称职的父亲，他能陪孩子玩所有的游戏，是孩子忠实的小伙伴。小头爸爸的耐心和细心是罕见的，他能和儿子钻进一个特大的纸壳子里，玩两座小房子的游戏。在给予大头儿子足够想象力空间的同时也满足了他自己的一颗童心。围裙妈妈: 家庭主妇，任劳任怨，擅长烹饪和唠叨，深爱着儿子和老公。是爸爸和儿子的连接点。也是父子两的主要话题来源，经常都是父子两如何一起出谋划策讨围裙妈妈开心。



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""


# --- 《大头儿子小头爸爸2》提示词模板 ---
DaTouErZi2_PROMPT_TEMPLATE = """
翻译要求：将电影《大头儿子小头爸爸2》中文剧本译为美式英语配音稿。需确保：
 
1. 源语言：汉语 目标语言：美式英语 
2. 将中文台词译为美式英语，保持非正式活泼风格，
3. 角色名参考原片设定（Big-Head Son/Small-Head Dad/Apron Mom/Dr. Wang）。
4. 译文行数须与中文原文严格对齐，允许±5%行数浮动。台词需符合PG分级标准，避免成人化表达。
5. 人物性格需通过对话体现：Big-Head Son顽皮机灵，Small-Head Dad憨厚幽默，Apron Mom急性子但暖心，Dr. Wang用伪科学术语包装阴谋。
6. 科技元素台词保留趣味性，如"一日成才"译为"One-Day Genius Program"。
 
7.剧情背景介绍：Big-Head Son, though bright and well-mannered, can’t resist his playful nature, neglecting his studies, much to the distress of Apron Mom. One day, Small-Head Dadencounters Dr. Wang , who offers a “One-Day Genius” program to instantly create prodigies. Hoping to shape her son, Apron Mom enrolls him, initially delighted by the outcome. But as flaws appear in Big-Head Son, Dr. Wang’s dark scheme slowly unravels.



8.人物身份：大头儿子: 天性爱玩，被许多家长贴上“一个不可能成功的笨孩子”的标签，王博士为了证明自己拥有改变他人智力并让其走向成功的能力，将大头儿子选为“一日成才”计划的实验者。短时间内发生了神奇的改变。在“一日成才”计划下，大头儿子失去了感受爱和快乐的能力，不再温暖可爱，他表情严肃，眼神犀利，拥有了超能力的他并不快乐。小头爸爸: 大头儿子的父亲。儿子在接受“一日成才”计划后性情大变，小头爸爸陷入了伤心与自责。当小头爸爸脑海中再次浮现神秘人物 “成功，就要付出代价”的论断时，他决意“爸气”对决：用父爱来换回自己懂事的儿子。围裙妈妈: 因为儿子对课外学习不屑一顾，围裙妈妈陷入了对儿子未来的焦虑之中。围裙妈妈启动了“精英养成模式”，让大头儿子开启了“小小上班族”的补课生活。在遇到打出成功标语“只要找到我，你的孩子就可以马上成功”的王博士后，便将大头儿子交给王博士，去做“一日成才”计划的实验者。王成功: “一日成才”计划的推动者，他对“成功学”的崇拜已经到了痴迷的状态。王博士巧妙抓住家长们“望子成龙，望女成凤”的心理，引导家长加入自己的“一日成才”计划。


请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""




# --- 《鹿鼎记》提示词模板 ---
LuDingJi_PROMPT_TEMPLATE = """
翻译要求：将电影《鹿鼎记》中文剧本译为美式英语配音稿。需确保：
 
1.将香港经典喜剧电影《鹿鼎记2：神龙教》剧本译为美式英语，唇形同步需精准匹配开口闭口帧，音节数与停顿节点对齐原台词波形。
角色塑造需突出韦小宝（Wilson Bond）的市井机灵与陈近南的侠义反差，台词节奏保留周星驰式急停急起的无厘头韵律。
译文字幕行数严格对应原文字幕时间轴，PG-13分级语境适配（例："抓奶龙爪手"译为Claw of the Milky Dragon）。
势力名称保留威妥玛拼音（神龙教Shenlong Sect/天地会Tiandihui）。韦小宝七位夫人台词需体现各自动物化特征（建宁公主的刁蛮用spicy，双儿的温婉用honey-dipped）。俚语库需含1992年香港街头黑话的美式对应表达（例：龟公pimp/敲竹杠shake down）。

2.特殊术语和人物角色表达直接使用术语对照表翻译后的内容
 
3.剧情背景介绍：Here’s the background for this film. It’s a Hong Kong classic comedy movie, The Deer and the Cauldron 2: Dragon Sect, starring Stephen Chow, telling the story of Wilson Bond, a witty and hilarious underdog navigating between the emperor, the martial world, and his multiple wives. In this film, Wilson Bond maneuvers among forces like Kangxi, the Dragon Sect, tiandihui, Wu Sangui, and more, while dealing with his romantic entanglements. Please translate this film’s script into American English for lip sync dubbing. Pay attention to the open mouth and close mouth words at the beginning and end of each sentence, keeping syllables and pauses as close as possible to the original lines, and fine-tune the rhythm and dialogue flow of the scripts. Focus on character building for Wilson Bond and Chen Jinnan, etc. The overall tone for this film should be witty, humorous and entertaining.



4.人物身份：韦小宝出身于市井烟花柳巷，没有知识、没有文化、也没有武功，专会溜须拍马、投机钻营、见风使舵，但是却能飞黄腾达、官运亨通，甚至娶了令当时达官贵人阶层和市民阶层都为之眼红——七个如花似玉的老婆！中国人的缺点、优点，各种东西都集中在韦小宝这个经典人物的身上。龙儿：神龙教主洪安通的妻子，神龙教中的风云人物，天生丽质，生性风骚，懂得美化和突出自己，充满自信，因而显得格外光彩照人，后来成为韦小宝的妻子。在韦小宝得7个老婆中，她的年龄最大、武功最高、见识最多、个性最强，从而是韦小宝的“夫人团”中的天然的团长和领导人。有时候，韦小宝也不得不听她的，因为她不但曾经是韦小宝的上司，而且也确实最有才干，最可能成为韦小宝人生和事业的最佳助手和重要的军师，甚至，是韦小宝的真正的大姐和老师。康熙(顺治皇帝的第三子)偶然与韦小宝相识，并因摔跤摔出与主人公韦小宝一段难得的交情，但是后来因为韦小宝识破天子之身，他们的关系大为改变。康熙皇帝表现出对韦小宝这位宠臣似徒弟似朋友般独一无二的关怀，实际上，一是要将韦小宝当作自己的“化身”显露少年康熙喜欢冒险喜欢新鲜事，遇到大事，总跃跃欲试，想亲身去体验一下，来验证自己的能力的少年天性，而且在皇帝的光环下满足一个 小皇帝强烈的好奇心；二是作为异常精明能干的皇帝,康熙不仅吸收了封建统治者御治术的精华,但同时也要不得不罩上一层礼义廉耻,仁义道德的伪善的外衣与神圣的光环，通过韦小宝之手去不择手段、寡廉鲜耻的达到帝王目的,实现自己一个个的政治目的。双儿是庄家的丫环，韦小宝的妻子和忠实伴侣，吴六奇的干妹妹。，性情柔顺，心灵手巧，尤其是武功高强，多次舍生忘死保护韦小宝。她没有自己的姓，只知道她的名字叫双儿。她没有自己的生活，韦小宝的一切便是她的一切。韦小宝带着她，她便精心照料，心满意足。韦小宝仍下她，她便日思夜想，愁眉不展。韦小宝在少林寺出家的时候，她就住在山下守侯，韦小宝南争北战时，她混在军中听用。在韦小宝身边的七个女人中，他对双儿最为关心，最为亲厚，最为真情，也最为情深意切。当然，在这些人中，也只有双儿，对韦小宝最为忠诚、无条件的娴淑、无限量的温柔、无止境的感恩图报。7个女人中，韦小宝最舍不得的就是双儿。建宁公主，皇帝康熙的妹妹。却不是真正的皇后（即后来的皇太后）所生，而是冒充皇后/皇太后的毛东珠所生。建宁公主的身份很尊贵，但却荒唐残忍，而这个公主的性格出奇的施虐狂，在下嫁吴应熊的途中，竟然设计与赐婚使者韦小宝勾搭成奸。在韦小宝所有的妻子之中，唯有这个假公主对韦小宝采取主动，原因未必是出于爱情，只是因为只有这个韦小宝敢辱骂她。韦小宝的7位夫人之中，与韦小宝最早发生关系的是她，韦小宝最“怕”的是她，韦小宝最不喜欢、甚至最看不起的也是她。皇宫之中，无拘无束地成长为一个“野丫头”便是——建宁公主。阿珂：陈圆圆和李自成的女儿，九难师太的弟子，郑克爽的情人，最终是韦小宝的妻子。阿珂是韦小宝所遇到的女孩子中形象最美丽、身份最神秘、命运最诡异、性格最倔强、情感最强烈、心智最浅薄的一个。但是她心中爱慕的是那个台湾的郑三公子，可是韦小宝偏偏具有一种顽强的精神，他第一是发毒誓，坦明自己的心迹，同时是鼓励自己的信心，然后就利用一切机会，来不择手段地达到目的。但是阿珂永远没有爱上过韦小宝。陈近南是第二代延平郡王郑经长子郑克臧的岳父。陈近南乃是韦小宝的恩师之一，曾经以内力帮助小宝驱除海公公所下的剧毒，实对韦小宝有再造之恩，其“凝血神抓”也是盖世绝学，又为天地会总瓢把子，所以江湖上名头甚大，有“为人不识陈近南，便称英雄也枉然”的说法。表面上，韦小宝是陈近南的下属，又是陈近南的弟子，而在内心深处，韦小宝实际上是把陈近南当成了自己的父亲

翻译术语对照表：

韦小宝	Wilson Bond	
吴应熊	Wu Yingxiong	
天地会	tiandihui	
平西王	King of West	
狗皇帝	You tyrant	
寒冰掌	Ice Palm!	
神龙教	the Dragon Sect	
丽春院	Li Chun Brothel	
韦大人	Lord Wilson	
神龙教主	the Dragon Master	
多隆	Duo Long	
多大人	Lord Duo	
反清复明	Down with Qing—up with Ming!	
青木堂	Green Wood Hall	
堂主	leader	
小宝	Will	康熙叫他Will 建宁等情人叫他Willy
栖凤楼	Phoenix Pavilion	



请严格按照上述要求，只将下面这一行中文文本翻译成美式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""



# --- 《宁安如梦》提示词模板 ---
NingAnRuMeng_PROMPT_TEMPLATE = """
翻译要求：将电视剧《宁安如梦》中文剧本译为英式英语配音稿。需确保：
 

一些特殊角色或者命名参考翻译术语对照表，例如：宁安如梦 Story of Kunning Palace
1. 角色身份非正式命名： 
- 姜雪宁 Jiang Xuening（重生黑莲花） 
- 谢危 Xie Wei（腹黑帝师） 
- 张遮 Zhang Zhe（白月光御史） 
- 燕临 Yan Lin（忠犬小侯爷） 
2. 翻译规范： 
• 闭口音词首选用/b/ /p/ /m/收尾词 
• 长元音匹配中文拖腔字 
• 爆破音对应中文顿挫处 
• 每句保留0.3秒气口间隙 
• PG13级含蓄处理亲密台词 
3. 韵律要求： 
- 抑扬格五步诗体改编权谋台词 
- 押头韵处理关键宣言 
- 尾韵强化情感爆发点 
- 疑问句保留升调悬念感 
4. 时代语料库： 
• 采用Tudor时期宫廷用语 
• 军事术语参照英法百年战争词典 
• 称谓使用My Lord/My Lady替代大人/娘娘 
5. 唇形参数： 
- 宽口型对应/æ/ /ɑː/音素 
- 窄口型匹配/iː/ /uː/发音 
- 双唇音特写镜头保留原台词字数

2.特殊术语和人物角色表达直接使用术语对照表翻译后的内容
 
3.剧情背景介绍：Here’s the background for the costume drama series, Story of Kunning Palace. Set in a richly woven ancient realm, it follows Jiang Xuening, a shrewd woman reborn with a chance to rewrite her fate, shedding her past wickedness to forge a virtuous path. Haunted by her previous life, she allies with Xie Wei, a brilliant yet tormented strategist, to thwart the rebellion of King of the West and his treacherous faction. Zhang Zhe, a principled scholar, quietly supports her redemption, while Yan Lin, a gallant noble, wrestles with his loyalty to her cause. As Jiang Xuening and Xie Wei confront palace conspiracies and personal shackles, their partnership deepens into a bond that defies all odds, leading them to overcome their burdens and unite as soulmates. Please translate this historical drama script into British English for lip-sync dubbing. Pay attention to open mouth and closed mouth words at the beginning and end of each sentence, aligning syllables and pauses with the original lines. Fine-tune the rhythm and dialogue flow for natural delivery.  Craft a tone that’s intricate, romantic, and triumphant.


4.人物身份：姜雪宁：姜家二小姐。前世姜雪宁费尽心机当上皇后，却在宫变中被逼自杀。重活一世后，她不再想做皇后，而是想着如何保燕家满门的性命，如何救尤芳吟与张遮不死，后来更是为了解救和亲的长公主沈芷衣，随谢危北上迎击来犯的敌国，过程中他们联手揭开了二十年前平南王事件的真相，两人也终成眷属。谢危：字居安，太子少师。谢危本是定国公府的世子薛定非，幼年时恰逢平南王作乱而被挟走，残酷的经历使其患上了离魂症。成年后的他在姜府的安排下，随姜雪宁一同入京，途中发病被雪宁喂血所救。谢危入京后仅用四年，就已成为当朝帝师。他智慧过人，手段狠辣，一开始与姜雪宁是针尖对麦芒，后被姜雪宁的爱感化。张遮：刑科给事中。张遮出身贫寒，前世他通过自己的努力，一步步升至刑部侍郎的高位，立志做一个好官的他，为了姜雪宁违背了自己的信仰，成为其谋取权力的重要助手。今生因为姜雪宁的主动靠近，两人的命运再次产生交集，却因为张遮母亲的意外离世，最终未能走到一起。燕临：勇毅侯府世子。燕临与姜雪宁是青梅竹马，他性格热情外放兼具坦荡爽朗，对姜雪宁一直都是无条件的维护、照顾，想成年后娶其过门，但血冠礼风波却改变了他的命运。做逍遥自在的世子时，燕临对姜雪宁的爱张扬至极；但当他蒙难时，唯恐波及他的宁宁，他选择回避，甚至放手。沈芷衣：乐阳长公主。前世沈芷衣喜欢上女扮男装的姜雪宁，在得知她是女子后，恼羞成怒对其百般刁难，后因远嫁和亲惨死。沈芷衣因眼角有一道当年平南王谋反时留下来的伤疤而自卑，姜雪宁重活一世后，帮她解开了这个心结，二人因此成为好友。因为肩负的责任，今生沈芷衣还是选择去和亲，临走时她留下一盒故土，等待他日雪宁带她回家。薛姝：定国公嫡女。薛姝遇事沉着冷静，凭借研香制茶之术，以及出众的才情，她在伴读课上屡屡获得上佳成绩。薛太后有意将其培养为未来的皇后，在薛太后的教导下她开始参与宫内斗争，并与张遮、谢危等人多次交锋。随着鹿纸计、香囊计接连失败，薛姝被家族抛弃，成为远嫁和亲的人选，万念俱灰之下，她选择投靠皇帝沈琅。

翻译术语对照表：

宁安如梦	Story of Kunning Palace
燕侯	Marquis Yan
世子	Viscount
万年老二	the Forever Runner-up
苏尚仪	Matron Su
内务府	Imperial Household Department
姜雪宁	Jiang Xuening
谢危	Xie Wei
张遮	Zhang Zhe
燕临	Yan Lin
平南王	Pingnan Wang
沈芷衣	Shen Zhiyi
薛姝	Xue Shu
尤芳吟	You Fangyin
沈玠	Shen Jie
姜雪慧	Jiang Xuehui
婉娘	Wan Niang
周寅之	Zhou Yinzhi
定国公府	Dingguo Duke’s Mansion
勇毅侯府	Yongyi Marquis’s Mansion
国公	Duke


请严格按照上述要求，只将下面这一行中文文本翻译成英式英语，并直接返回翻译结果，不要添加任何额外的解释或说明：
类似这种不需要返回：（注：根据技术规范要求，爆破音"bond"对应中文闭口字"和"，长元音"find"对应开口字"有"，音节数7:7完全匹配，维多利亚句式"be it...or"保留30%中文语序浪漫感，[!]标记气口与原声"好/局"停顿对齐）
直接返回翻译后的英文结果： This bond, be it[!] love or parting, must find its[!] end.
{text_to_translate}
"""






