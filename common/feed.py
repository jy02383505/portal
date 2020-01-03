
import aiohttp
import json
import requests
from django.utils.translation import ugettext as _
from django.conf import settings


DEFAULT_RULE_CONF = {'禁止空文件上传': 'Do not allow empty file uploads', '禁止非法的请求方式': 'Prohibit illegal request methods', '禁止安全扫描器扫描': 'Disable security scanner scanning', '执行cmd命令的跨站攻击规则': 'Cross-site attack rule for executing commands', '防止蠕虫病毒的远程文件存取': 'Prevent remote access of web crawling', '防止数据文件的远程文件存取': 'Prevent remote file access to data files', '攻击IIS服务器静态文件漏洞防御规则': "Defense rules for attacking IIS server static file's vulnerability", '利用UTF-7编码漏洞的XSS跨站攻击防御规则': 'Defense rules for XSS cross-site attack by using UTF-7 encoding vulnerabilities', '窃取源码的iis漏洞攻击防御规则': 'Defense rules for attack by stealing source code of iis vulnerability', '利用多个特殊符号进行IIS漏洞攻击防御规则': 'Defense rules for IIS attack with multiple special symbols', '防止二进制文件可执行文件的远程文件存取': 'Prevent remote file access to binary executables', '防止showcode获取代码内容的攻击规则': 'Rules that prevent attacks for showcode from getting code content', '防止java-servlet的漏洞攻击': 'Prevent java-servlet volnerabilities attach', '防止fckeditor的编辑器漏洞攻击规则': 'Rules prevent FCKeditor editor vulnerability attack', '防止利用转义符进行XSS跨站攻击的规则': 'Rules for preventing XSS cross-site attacks using escape characters', '防止利用javascript语法标签进行XSS跨站攻击的规则': 'Rules for preventing XSS cross-site attacks using javascript syntax tags', '防止利用vbscript语法进行XSS跨站攻击的规则': 'Rules for preventing XSS cross-site attacks using vbscript syntax', '防止利用javascript响应事件进行XSS跨站攻击的规则': 'Rules for preventing XSS cross-site attacks using javascript response events', '利用数字字符的sql注入攻击防御攻击规则': 'Defense rules for SQL injection attack using numeric characters', '利用http字段进行xss攻击的防御规则': 'Defense rules for xss attacks using the http field', '织梦内容管理平台变量漏洞防御规则': 'Defense rules for DedeCMS variable vulnerability', '禁止svn文件的远程文件访问': 'Disable remote file access for svn files', '禁止请求获取页面大小进行的远程文件访问': 'Prohibit requests for remote file access for page size', '禁止远程执行代码的远程文件访问规则': 'Rules against remote file access with remote code execution', '未限制文件扩展名的xss漏洞防御规则': 'Xss vulnerability defense rules for unrestricted file extensions', 'nginx/fastcgi的脚本漏洞防御规则': 'Defense rules for Nginx/fastcgi script vulnerability', '禁止动画以及图片类静态资源的远程文件访问规则': 'Rules for disable remote file access s for animation and image class static resources', 'nginx/fastcgi的php类文件漏洞防御规则': "Defense rules for Nginx/fastcgi php file's vulnerability", '利用页眉和脚注进行nginx漏洞攻击的防御规则': 'Defense rules for nginx vulnerabilities using headers and footers', '利用匹配汉字的错误进行sql注入攻击的防御规则': 'Defense rules for sql injection attacks using errors matching Chinese characters', '禁止上传关键字文件的规则': 'Rules against uploading keyword files', '利用php后缀文件触发nginx错误的漏洞规则': 'Defence rules for using php suffix file to trigger nginx error vulnerability', '利用Method关键词的远程执行漏洞防御规则': 'Defense Rules for remote execution vulnerability by using the Method keyword', '利用xml版本号进行远程文件访问的攻击防御规则': 'Defense rules for attack with remote file access using xml version number', '禁止上传带有请求方式关键词文件的规则': 'Rules against uploading keyword files with request mode', '利用java的属性标签进行的远程文件执行漏洞防御规则': 'Remote file execution vulnerability defense rules using java attribute tags', '利用多重脚本标签进行xss跨站攻击的防御规则': 'Defense rules for xss cross-site attacks using multiple script tags', '在x-forwarded-for中增加执行语句的sql注入攻击防御规则': 'Defense rules for adding sql injection attack or executing statements in x-forwarded-for', '利用iframe标签进行的xss跨站攻击防御规则': 'Defense rules for Xss cross-site attack using iframe tags', '利用script标签和页面等待事件进行的xss跨站攻击防御规则': 'Defense rules for Xss cross-site attack by using script tags and page wait events', '利用prompt响应进行xss跨站攻击防御的规则': 'Rules for defending xss cross-site attacks with prompt responses', '利用请求头中语言信息进行执行代码的xss跨站攻击防御规则': 'Defense rules for Xss cross-site attack executing code using language information in the request header', '利用&#符号进行的xss跨站攻击防御规则': 'Defense rules for Xss cross-site attack using &# notation', '利用请求头中客户端ip信息执行代码的sql注入攻击防御规则': 'Defense rule for the sql injection attack that executes the code by using the client ip information in the request header', '利用星号进行xss跨站攻击的防御规则': 'Defense rules for xss cross-site attacks using asterisks', '禁止上传带有文件操作符的关键字文件规则': 'Rules disable uploading keyword file with file operators', '禁止上传带有后门关键字的文件规则': 'Rules disable uploading files with backdoor keywords', '禁止上传带有passthru关键字的文件规则': 'Rules disable uploading filewith the passthru keyword', '防止利用spellchecker进行的sql注入攻击防御规则': 'Defense rules to prevent sql injection attack using spellchecker', '防止利用html标签和动作关键字进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using html tags and action keywords', '防止利用插入静态资源的标签进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using tags inserted into static resources', '防止利用javascript事件关键字进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using javascript event keywords', '防止利用libinjection进行sql注入攻击的规则': 'Rules to prevent sql injection attacks using libinjection', '防止利用多个<script>重叠标签进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using multiple <script> overlapping tags', '防御利用织梦数组关键词漏洞攻击的规则': 'Defense rules for DedeCms array keyword vulnerability attacks', '防止利用cookie中带有数据类型关键字进行跨站攻击的规则': 'Rules prevent the use of cookies with cross-site attacks with data type keywords', '防止利用cookie中增加位置标签关键字进行跨站攻击的规则': 'Rules prevent location tags from using cookies to increase cross-site attacks', '防止利用cookie中增加事件关键字进行跨站攻击的规则': 'Rules prevent the use of cookies to increase the number of event keywords for cross-site attacks', '防止在body数据中增加多个script标签和扫描关键字进行跨站攻击的规则': 'Rules to prevent cross-site attacks by adding multiple script tags and scan keywords to the body data', '禁止上传动态前端可执行文件的规则': 'Rules prevent for uploading dynamic front-end executables', '防止利用cookie中增加点击事件弹窗的跨站攻击规则': 'Rules prevent cross-site attack that increase the click event pop-up in cookies', '利用asp.net的oracle漏洞攻击的防御规则': 'Defense rules for exploiting asp.net oracle exploits', '防止上传带有创建对象关键字的文件规则': 'Rules that prevent uploading of file with the creation of object keywords', '防止在body数据中增加大量脏数据的防御规则': 'Defense rules that prevent adding large amounts of bad data in the body data', '防止在请求中增加非法的php文件名的防御规则': 'Defense rules to prevent illegal php filenames from being added to requests', '禁止上传带有assert关键字的防御规则': 'Defense rules to prevent illegal php filenames from being added to requests', '防止执行having判断的sql注入攻击规则': 'Rule against SQL injection attack to execute of having judgment', '防止执行backup备份操作的sql注入攻击规则': 'Rules prevent SQL injection attack to backup operations', '防止增加SomeCustomInjectedHeader关键字的攻击防御规则': 'Defense rules prevent attack from increasing the Some Custom Injected Header keyword', '防止获取上一个目录路径的攻击防御规则': 'Defense rules to prevent attack from getting the previous directory path', '防止长数据中带有鼠标操作关键字的xss跨站攻击规则': 'Rules prevent xss cross-site attack with mouse action keywords in long data', '防止利用response进行webshell提权的防御规则': 'Defense rules prevent the use of response for webshell privilege', '防止获取etc/passwd的远程文件获取攻击规则': 'Rules prevent remote file acquisition attack from getting etc/passwd', '防止远程执行InvokerServlet命令的规则': 'Rules to prevent remote execution of InvokerServlet commands', '防止获取odbc信息的sql注入规则': 'Rule to prevent SQL injection in odbc information', '防止利用织梦平台上传文件名漏洞攻击的规则': 'Rules prevent the use of the DedeCms platform to upload file name vulnerability attacks', '防止利用织梦平台获取附件大小漏洞攻击的规则': 'Rules prevent the use of the DedeCms platform to obtain attachment size exploits', '防止利用数据库关键文件名进行sql注入攻击的规则': 'Rules for preventing SQL injection attacks using database key file names', '防止利用休眠关键字在测试工具中进行sql注入攻击的规则': 'Rules for preventing SQL injection attacks in the test tool using the hibernate keyword', '防止利用select关键字在测试工具中进行sql注入攻击的规则': 'Rules for preventing SQL injection attacks in the test tool using the select keyword', '防止在cookie中增加可执行sql信息语句进行sql注入攻击的规则': 'Rule prevent adding executable sql information statements to the SQL to inject attack in the cookie', '防止利用常量数值进行sql注入攻击的规则': 'Rules to prevent the use of constant values for SQL injection attacks', '防止利用case+like+having的组合语句进行sql注入攻击的规则': 'Rules to prevent the use of case + like + having combination statement for sql injection attackto', '防止利用设置变量类型进行sql注入攻击的规则': 'Rules for prevent the setting SQL injection attacks by setting variable types', '防止利用合并数据库语句进行sql注入攻击的规则': 'Rules for preventing SQL injection attacks using merged database statements', '防止利用select+union的组合语句进行sql注入攻击的规则': 'Rules to prevent sql injection attack by using the combined statement of select+union', '防止执行关闭数据库语句的sql注入攻击规则': 'Rules to prevent the execution of SQL injection attack that close database statements', '防止利用比较运算符触发sql报错的sql注入攻击规则': 'Prevent sql injection attack rules that use the comparison operator to trigger sql error reporting', '防止利用存储过程关键字触发sql报错的sql注入攻击规则': 'Rules against SQL injection attack that use stored procedure keywords to trigger SQL error reporting', '防止利用创建函数关键字触发sql报错的sql注入攻击规则': 'Rules to prevent the sql injection attack triggers sql error by using the create function keyword', '防止利用联合查询语句进行sql注入攻击的规则': 'Rules for preventing sql injection attacks using joint query statements', '防止在sql语句中插入shell执行代码攻击的规则': 'Rules to prevent inserting shell execution code attacks in sql statements', '防止利用特殊符号触发正则表达式的sql注入攻击的规则': 'Rules for preventing sql injection attacks that trigger regular expressions with special symbols', '防止利用like语句执行shell命令的sql注入攻击规则': 'Rules to prevent sql injection attack for executing shell commands with like statements', '防止利用数据库内建函数特殊字触发的sql注入攻击规则': 'Rules to prevent sql injection attack triggered by special words in database built-in functions', '防止利用admin关键字获取管理员信息的sql注入攻击规则': 'Rules to prevent Sql injection attack to administrator information from being obtained by using the admin keyword', '防止利用执行sql命令触发sql报错的sql注入攻击规则': 'Rules to prevent the sql injection attack that triggers sql error by executing the sql command', '防止执行复合sql操作语句触发sql报错的sql注入攻击规则': 'Rules to prevent execution of compound sql operation statement trigger sql error sql injection attack', '防止利用distinct执行sql语句获取数据库信息的注入攻击规则': 'Rules to prevent injection attack that use distinct to execute sql statements to obtain database information', '防止利用when等关键词进行sql信息获取的sql注入攻击规则': 'Rules to prevent sql injection attack for using sql information to obtain keywords such as "when"', '防止利用多个并列条件触发sql报错的sql注入攻击规则': 'Rules to prevent sql injection attack that use multiple parallel conditions to trigger sql error reporting', '防止使用特殊符号触发多个查询条件获取sql信息的sql注入攻击规则': 'Rule to prevent SQL injection attack that use of special symbols to trigger multiple query conditions to obtain sql information', '防止select和多种标签的阶段2sql注入攻击': 'Rules for prevent phase 2sql injection attack to select and multiple tags', '防止执行命令符号和多种标签的阶段2sql注入攻击': 'Rules for stage 2sql injection attack to prevent execution of command symbols and multiple tags', '防止种下执行命令cookie代码的sql注入攻击': 'Rules to prevent sql injection attacks that execute the command cookie code', '防止使用多个or关键字进行sql注入攻击的规则': 'Rules for preventing sql injection attacks using multiple "or" keywords', '防止使用多个and关键字进行sql注入攻击的规则': 'Rules for preventing sql injection attacks using multiple "and" keywords', '防止利用拆分组合关键字的方式进行sql注入攻击的规则': 'Rules for preventing sql injection attacks by splitting combined keywords', '防止利用sql注释进行sql注入攻击的规则': 'Rules for preventing sql injection attacks using sql comments', '防止使用16进制转义进行sql注入攻击的规则': 'Rules for preventing sql injection attacks using hexadecimal escaping', '防止利用连续4个非字符进行命令执行的sql注入规则': 'Rules for prevent sql injection for command execution using 4 consecutive non-characters', '防止利用拼接script标签正则进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using spliced script tags', '防止利用16进制转义形成响应事件的xss跨站攻击规则': 'Rules to prevent xss cross-site attack that use hexadecimal escaping to form response events', '防止利用获取系统信息方式进行xss跨站攻击的规则': 'Rules to prevent for xss cross-site attacks by acquiring system information', '防止在标签中嵌入拼接注释script方式进行xss跨站攻击的规则': 'Rules for preventing splicing annotation scripts from being embedded in tags for xss cross-site attacks', '防止在style标签中增加链接弹窗的xss跨站攻击规则': 'Rules to prevent xss cross-site attack for adding link pop-ups in style tags', '防止注释被转义之后形成script标签的xss跨站攻击规则': 'Rules to prevent xss cross-site attacks with script tag from comments being aliased', '防止script标签中嵌套注释信息带有script标签的xss跨站攻击规则': 'Rules to prevent xss cross-site attacks with nested comment information in script tags with script tags', '防止使用拼接方式生成数据信息触发报错的xss跨站攻击规则': 'Rules to prevent xss cross-site attacks by triggering data error from using splicing method to generate data information', '防止在style标签中使用颜色代码进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using color codes in style tags', '防止使用frame标签指定src进行xss跨站攻击的规则': 'Rules to prevent xss cross-site attacks by using frame tags to specify src', '防止使用颜色代码和列表格属性进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using color code and list grid attributes', '防止使用颜色代码和表格划线的方式进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using color codes and table lines', '防止利用插入多媒体文件进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks by inserting multimedia files', '防止利用namespace载体进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using namespace carriers', '防止使用meta连接url的跨站攻击的规则': 'Rules for preventing cross-site attacks using meta connection urls', '防止使用meta插入字符集进行xss跨站攻击的规则': 'Rules to prevent xss cross-site attacks using meta-inserted character sets', '防止使用远程样式表的方式进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using remote style sheets', '防止使用BASE标签连接url进行跨站攻击的规则': 'Rules for preventing cross-site attacks using BASE tag connection urls', '防止利用APPLET绕过发送xss-email的xss跨站攻击的规则': 'Rules to prevent attacks using APPLET to bypass the xss cross-site that send xss-email', '防止利用OBJECT进行表单欺骗的xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using form spoofing with OBJECT', '防止利用ASCII编码进行xss跨站攻击的规则': 'Rules for preventing xss cross-site attacks using ASCII encoding', '利用不完整标签拼接非字符进行XSS跨站攻击的防御规则': 'Defense rules for XSS cross-site attacks using incomplete label splicing non-characters', '利用utf8解码拼接关键词进行xss跨站攻击的防御规则': 'Defense rules for xss cross-site attacks using utf8 decoding splice keywords', 'IE浏览器XSS攻击探测规则': 'Rules for IE browser XSS attack detection', '目录遍历防御规则': 'Rules for directory traversal defense rules', '防止利用ip的url进行远程文件包含的规则': 'Rules to prevent the use of ip url for remote file inclusion', '防止利用远程包含配置文件获取服务器信息的规则': 'Rules to prevent for obtaining server information using remote include profiles', '防止利用问号通配符进行远程文件包含的规则': 'Rules to prevent for remote file inclusion using question mark wildcards', '防止利用域名链接进行远程文件包含的规则': 'Rules to prevent the use of domain name links for remote file inclusion rules', '防止利用php的指示标签进行php注入攻击的规则': "Rules to prevent for php injection attacks using php's indicator tag", '防止利用php读写文件代码进行php注入攻击的规则': 'Rules to prevent the use of php read and write file code for php injection attacks', '防止在html中设置cookie进行会话固定请求的规则': 'Rules to prevent cookies from being set in html for session fixation requests', '防止利用文件头信息进行http请求嗅探的规则': 'Rules for preventing http request sniffing using file header information', '防止利用CR/LF和http请求方法组合进行http请求头走私的规则': 'Prevent the use of CR/LF and http request methods to combine http request header smuggling rules', '防止利用CR/LF字符进行http请求头截断走私的规则': 'Rules for preventing http request header truncation attacks using html information in http', '防止利用http中html信息进行http请求头截断攻击的规则': 'Rules for preventing http request header truncation attacks using html information in http', '防止利用http请求头中的CR/LF字符进行http请求头注入攻击的规则': 'Rules for preventing http request header injection attacks using CR/LF characters in the http request header', '防止在请求中利用CR/LF字符进行请求头注入攻击的规则': 'Rules for preventing request header injection attacks using CR/LF characters in requests', '防止利用CR/LF字符和header变量进行请求头注入攻击的规则': 'Rules for preventing request header injection attacks using CR/LF characters and header variables', '防止利用ApacheStruts2的JakartaMultipartparser插件漏洞进行远程代码执行的规则': 'Rules to prevent rules for remote code execution using the Jakarta Multipart parser plugin vulnerability in Apache Struts2', '防止利用ApacheStruts2的JakartaMultipartparser插件在处理文件上传时的漏洞进行远程代码执行的规则': "Rules for preventing the use of Apache Struts2's Jakarta Multipart parser plugin for handling remote file execution loopholes in file uploading", '防止通过LDAP命令进行注入攻击的规则': 'Rules to prevent injection attacks through LDAP commands', '防止NginxFastcgiPHP文件解析漏洞发起攻击的规则': 'Rules to prevent Nginx Fastcgi PHP file parsing vulnerabilities from launching attacks', '防止系统敏感文件访问的规则': 'Rules to prevent system sensitive file access', '防止通过多次转义进行的远程Unix命令执行攻击规则': 'Rules to prevent remote Unix command execution attacks by multiple escaping', '防止通过多次转义进行的远程Unix命令执行攻击规则2': 'Rules to prevent remote Unix command execution attacks by multiple escaping 2', '防止通过转义拼接形成windows命令执行攻击规则': 'Rules to prevent the formation of windows command execution attacks by escaping splicing', '防止通过转义拼接形成windows命令执行攻击规则3': 'Rules to prevent the formation of windows command execution attacks by escaping splicing 3', '防止WindowsPowerShell命令注入攻击规则': 'Rules to prevent Windows PowerShell command injection attacks', '防止Unix关键字Shell注入攻击的规则': 'Rules to prevent Unix keyword shell injection attacks', '使用libinjection引擎拦截XSS攻击': 'Intercept XSS attacks using the libinjection engine', '拦截webshell攻击规则': 'Intercept webshell attack rules', '防止通过and/or进行SQL注入点试探': 'Prevent SQL injection point testing through and/or'}


WAF_ATTACK_TYPE = {
    'DedeCms': '织梦模板漏洞攻击',
    'FCKEditor Vulnerabilities': 'FCK编辑器漏洞攻击',
    'File Upload': '非法文件上传',
    'HTTP Header Injection': 'HTTP请求头注入',
    'HTTP Request Smuggling': 'HTTP请求混淆攻击',
    'HTTP Response Splitting': 'HTTP响应拆分攻击',
    'Illegal Request Method': '非法的请求方法',
    'Microsoft IIS Vulnerabilities': 'IIS漏洞攻击',
    'nginx fastcgi/php vulnerability': 'fastcgi/php漏洞攻击',
    'Nginx vulnerability': 'nginx漏洞攻击',
    'Nil Post': '空文件上传',
    'OS File Access': '系统文件获取',
    'Other': '其他类型',
    'other': '其他类型',
    'Path Traversal Attack': '文件目录遍历',
    'PHP Injection Attacks': 'PHP注入攻击',
    'Remote Command Execution': '远程命令执行',
    'Remote File Access': '远程文件获取',
    'Remote File Execution': '远程文件执行',
    'Remote File Inclusion': '远程文件包含',
    'Security Scanner Scanned': '扫描器扫描',
    'SQL Injection Attack': 'SQL注入攻击',
    'User Defined WAF Rules': '用户自定义防护规则',
    'Web Struct Vulnerabilities': '网站框架漏洞攻击',
    'Webshell': 'Webshell',
    'XSS Attack': 'XSS跨站',
}


class AccountsFeed:
    """账户信息描述"""
    # 内部名称
    ADMIN = _('管理员')
    CUSTOMER_SERVICE = _('客服')
    COMMON_STAFF = _('普通员工')
    CUSTOMER = _('客户')
    CUSTOMER_CHILD = _('客户子账号')
    CLIENT = _('客户端')
    MANAGER = _('管理端')

    COMMON = _('通用')

    SYSTEM_PERM_STRATEGY = _('系统策略')
    PARENT_PERM_STRATEGY = _('自定义策略')

    # 消息返回
    PARAME_ERROR = _('参数错误')
    USERNAME_EMPTY = _('账号名称不能为空')
    USER_EXIST = _('用户已经存在')
    USER_NOT_EXIST = _('用户不存在')
    PASSWORD_EMPTY = _('账号密码不能为空')
    COMPANY_EMPTY = _('公司名不能为空')
    USER_ERROR = _('账号名或密码错误')
    USER_LOCKING = _('账号已被锁定')
    USER_NOT_ACTIVE = _('账号没有激活')
    GROUP_EMPTY = _('角色不存在')
    GROUP_NAME_EMPTY = _('角色名称不能为空')
    GROUP_ALREADY_EXIST = _('角色已存在')
    GROUP_HAS_USER = _('角色下还有用户,请清空后再删除')

    COMMON_CUSTOMER = _('普通用户')
    AGENT_CUSTOMER = _('代理用户')
    CHILD_CUSTOMER = _('子用户')

    IS_ACTIVE = _('启用')
    IS_NOT_ACTIVE = _('禁用')

    PERM_STRATEGY_NAME_EMPTY = _('策略名称不能为空')
    PERM_LIST_EMPTY = _('权限列表不能为空')
    PERM_STRATEGY_NOT_EXIST = _('策略不存在')

    DOMAIN_NOT_EXIST = _('域名不存在')
    DOMAIN_EXIST = _('域名已存在')
    CERT_NAME_EMPTY = _('证书名不能为空')
    PROTOCOL_EMPTY = _('域名协议不能为空')
    SRC_BACK_TYPE_EMPTY = _('备回源类型不能为空')
    CERT_NAME_EMPTY = _('证书名不能为空')
    CERT_VALUE_OR_KEY_EMPTY = _('证书内容与key不能为空')
    CERT_EMAIL_EMPTY = _('证书邮箱不能为空')

    URL_FORMAT_ERROR = _('url格式不正确')
    SEND_ERROR = _('下发失败')
    MY_ACCOUNT = _('我的账号')

    PROTOCOL_FORMAT_ERROR = _('协议格式不正确')
    CACHE_FORMAT_ERROR = _('缓存格式不正确')


class OperateMsg(object):
    """操作日志"""
    ACCOUNTS = '用户操作'

    LOGIN_SYSTEM = '用户登录'
    LOGIN_LDAP_SYSTEM = '用户通过ldap校验登录'
    LOGIN_LDAP_REGISTER = '用户通过ldap校验创建用户'
    CREATE_USER = '%s创建用户>%s(%s)'
    EDIT_USER = '%s修改用户>%s'
    CREATE_GROUP = '%s创建角色>%s'
    EDIT_GROUP = '%s修改角色>%s'
    DELETE_GROUP = '%s删除角色>%s'
    CREATE_PERM_STRATEGY = '%s创建了权限策略>%s(%s)'
    DELETE_PERM_STRATEGY = '%s删除了权限策略>%s(%s)'
    OPEN_API = '%s开通API秘钥>%s'
    OPEN_SET_API_STATUS = '%s设置了api状态>%s'
    REMOVE_API = '%s关闭API秘钥>%s'

    SECURITY = '安全操作'
    CREATE_SECURITY_DOMAIN = '%s创建安全频道>%s'
    CREATE_SECURITY_USER = '%s创建安全用户>%s'
    SET_DEFAULT_RULE_MODE = '%s设置域名%s默认规则模式>%s'
    SET_SELF_RULE_MODE = '%s设置域名%s自定义规则模式>%s'
    RESET_DEFAULT_RULE = '%s设置域名%s默认规则>%s'

    ENABLE_DEFAULT_RULE = '%s设置域名%s默认规则%s>%s'
    ENABLE_SELF_RULE = '%s设置自定义规则%s>%s'

    CREATE_WAF_DOMAIN = '%s创建了waf域名%s'
    BINDING_WAF_DOMAIN = '%s绑定了waf域名%s'
    EDIT_WAF_CONF = '%s修改%s的waf配置'
    SET_WAF_CDN_STATUS = '%s设置%s的waf的CDN状态为%s'
    SET_WAF_STATUS = '%s设置%s的waf的状态为%s'
    UPLOAD_WAF_CERT = '%s上传了waf的证书%s'
    BINDING_USER_CONTRACT = '%s为%s绑定了合同>%s'

    SET_CDN_BASE_CONF = '%s设置了%s的CDN基础配置'
    CREATE_CDN_DOMAIN = '%s为%s创建了域名%s'
    EDIT_CDN_DOMAIN = '%s为%s修改了域名%s'
    DISABLE_CDN_DOMAIN = '%s为%s报停了域名%s'
    ACTIVE_CDN_DOMAIN = '%s为%s激活了域名%s'


class SecWafConf(object):
    """waf 配置信息"""

    WAF_ORIGIN = 'hpc200-04-HKonly.ccna.ccgslb.com'

    BASE_TOKEN = 'ffb622b758475ede6bded7c356e981'

    WAF_DEFAULT_MODE_CONF = [
        {'id': 0, 'cname': _('关闭')},
        {'id': 1, 'cname': _('普通模式')},
        {'id': 2, 'cname': _('严防模式')},
        {'id': 3, 'cname': _('观察模式')},
    ]

    WAF_SELF_MODE_CONF = [
        {'id': 0, 'cname': _('关闭')},
        {'id': 1, 'cname': _('普通模式')},
    ]

    ACCESS_POINT_CONF = {
        'GZ': {'name': _('广州'), 'cname': 'cc-waf-gz.ccgslb.com.cn'},
        'HK': {'name': _('香港'), 'cname': 'cc-waf-rim.ccgslb.com.cn'},
        'ML': {'name': _('大陆节点'), 'cname': 'cc-waf-mainland.ccgslb.com.cn'},
        'MT': {'name': _('交通运输部特殊端口专用'),
               'cname': 'cc-waf-mainland-jtb.ccgslb.com.cn'},
    }

    ACCESS_TYPE_CONF = [
        {'id': 1, 'name': '上层>waf>源站'},
        {'id': 2, 'name': '边缘>waf>上层'},
    ]

    SRC_TYPE_IP = 1
    SRC_TYPE_DOMAIN = 2
    SRC_TYPE_CONF = [
        {'id': SRC_TYPE_IP, 'name': 'ip回源'},
        {'id': SRC_TYPE_DOMAIN, 'name': '域名回源'},
    ]

    DOMAIN_AUDIT_FAILED = '域名审核不通过'
    DOMAIN_WAIT_AUDIT = '域名等待审核'
    DOMAIN_CHECK_FAILED = '操作异常'
    WAF_TOKEN_EMPTY = 'token不存在'


class CDNConf(object):
    """cdn 配置信息"""
    # BASE_CC_CMS_TEMPLATE_ID = '1068'
    BASE_CC_CMS_TEMPLATE_ID = '1133'

    BASE_CNAME = ".ns.xgslb.com"

    CC = 'CC'
    TENCENT = 'TENCENT'

    OPT_CONF = [
        {'id': CC, 'name': '蓝汛'},
        # {'id': tencent, 'name': '腾讯'}
    ]

    CMS_ANA_TEMPLATE_1 = 1
    CMS_ANA_TEMPLATE_2 = 2

    CMS_ANA_TEMPLATE = [
        {'id': CMS_ANA_TEMPLATE_1, 'name': _('通用自助模板')},
        {'id': CMS_ANA_TEMPLATE_2, 'name': _('泛模板')}
    ]

    WEB_CDN = 'web'
    DOWNLOAD_CDN = 'download'
    VOD_CDN = 'vod'

    NOVA_TYPE = '融合'
    NOVA_TYPE_LIST = [WEB_CDN, DOWNLOAD_CDN, VOD_CDN]

    CDN_TYPE = [
        {'id': WEB_CDN, 'name': _('页面加速'), 'check_name': '网页'},
        {'id': DOWNLOAD_CDN, 'name': _('下载加速'), 'check_name': '下载'},
        {'id': VOD_CDN, 'name': _('点播加速'), 'check_name': '点播'},
    ]

    CDN_TYPE_VIEW = [
        {'id': '', 'name': _('全部类型'), 'check_name': '点播'},
        {'id': WEB_CDN, 'name': _('页面加速'), 'check_name': '网页'},
        {'id': DOWNLOAD_CDN, 'name': _('下载加速'), 'check_name': '下载'},
        {'id': VOD_CDN, 'name': _('点播加速'), 'check_name': '点播'},
    ]

    HTTP_TYPE = 'http'
    HTTPS_TYPE = 'https'

    PROTOCOL_TYPE = [
        {'id': HTTP_TYPE, 'name': 'HTTP'},
        {'id': HTTPS_TYPE, 'name': 'HTTPS'}
    ]

    SRC_IP = 'ip'
    SRC_DOMAIN = 'dmn'

    SRC_TYPE = [
        {'id': SRC_IP, 'name': _('IP回源')},
        {'id': SRC_DOMAIN, 'name': _('域名回源')}
    ]

    SRC_BACK_IP = 'ip'
    SRC_BACK_DOMAIN = 'dmn'

    SRC_BACK_TYPE = [
        {'id': SRC_BACK_IP, 'name': _('IP')},
        {'id': SRC_BACK_DOMAIN, 'name': _('域名')}
    ]

    SUFFIX = 'suffix'
    PATH = 'path'

    CACHE_TYPE = [
        {'id': SUFFIX, 'name': _('文件')},
        {'id': PATH, 'name': _('文件夹')},
    ]

    DEFAULT_CACHE = {
        WEB_CDN: [
            {
                "TTL": 0,
                "type": SUFFIX,
                "urls": "php;aspx;asp;jsp;do;dwr;cgi;fcgi;action;ashx;axd;json"
            }, {
                "TTL": 7 * 24 * 3600,
                "type": SUFFIX,
                "urls": ("js;css;aif;apk;avi;bin;bmp;cab;doc;eot;exe;flv;gif;"
                         "gz;ico;ini;jpe;jpeg;jpg;m4a;mov;mp3;mp4;mpeg;mpg;msi;"
                         "pdf;png;otf;rar;svg;swf;ttf;txt;vbs;wav;wmv;woff;"
                         "woff2;zip")
            }, {
                "TTL": 3600,
                "type": PATH,
                "urls": "/"
            },
        ],
        DOWNLOAD_CDN: [
            {
                "TTL": 0,
                "type": SUFFIX,
                "urls": "php;aspx;asp;jsp;do;dwr;cgi;fcgi;action;ashx;axd;json"
            }, {
                "TTL": 7 * 24 * 3600,
                "type": SUFFIX,
                "urls": ("js;css;aif;apk;avi;bin;bmp;cab;doc;eot;exe;flv;gif;"
                         "gz;ico;ini;jpe;jpeg;jpg;m4a;mov;mp3;mp4;mpeg;mpg;msi;"
                         "pdf;png;otf;rar;svg;swf;ttf;txt;vbs;wav;wmv;woff;"
                         "woff2;zip")
            }, {
                "TTL": 3600,
                "type": PATH,
                "urls": "/"
            },
        ],
        VOD_CDN: [
            {
                "TTL": 0,
                "type": SUFFIX,
                "urls": "php;aspx;asp;jsp;do;dwr;cgi;fcgi;action;ashx;axd;json"
            }, {
                "TTL": 7 * 24 * 3600,
                "type": SUFFIX,
                "urls": ("js;css;aif;apk;avi;bin;bmp;cab;doc;eot;exe;flv;gif;"
                         "gz;ico;ini;jpe;jpeg;jpg;m4a;mov;mp3;mp4;mpeg;mpg;msi;"
                         "pdf;png;otf;rar;svg;swf;ttf;txt;vbs;wav;wmv;woff;"
                         "woff2;zip")
            }, {
                "TTL": 3600,
                "type": PATH,
                "urls": "/"
            },
        ],
    }

    DOMAIN_CREATING = 1
    DOMAIN_SERVING = 2
    DOMAIN_EDITING = 3
    DOMAIN_STOPPING = 4
    DOMAIN_DIS_CNAME = 5
    DOMAIN_DNS_TASK_EFFECT = 6
    ACTIVATING = 7
    DOMAIN_ERROR = -1

    DOMAIN_STATUS = [
        {'id': [DOMAIN_CREATING, DOMAIN_EDITING, DOMAIN_DIS_CNAME, DOMAIN_DNS_TASK_EFFECT, ACTIVATING], 'name': _('配置中')},
        {'id': [DOMAIN_SERVING], 'name': _('已启动')},
        {'id': [DOMAIN_STOPPING], 'name': _('已关闭')},
        {'id': [DOMAIN_ERROR], 'name': _('下发失败')},
    ]

    DOMAIN_STATUS_VIEWS = [
        {'id': [DOMAIN_CREATING, DOMAIN_EDITING, DOMAIN_DIS_CNAME, DOMAIN_DNS_TASK_EFFECT, ACTIVATING], 'name': _('配置中')},
        {'id': [DOMAIN_SERVING], 'name': _('已启动')},
        {'id': [DOMAIN_STOPPING], 'name': _('已关闭')},
        {'id': [DOMAIN_ERROR], 'name': _('下发失败')},
    ]

    REFRESH_CONDUCT = 0    # 刷新进行
    REFRESH_SUCCESS = 1    # 刷新成功
    REFRESH_FAIL = 2    # 刷新失败

    REFRESH_STATUS = [
        {'id': REFRESH_CONDUCT, 'name': _('刷新中')},
        {'id': REFRESH_SUCCESS, 'name': _('成功')},
        {'id': REFRESH_FAIL, 'name': _('失败')},
    ]

    REFRESH_URL = 'url'
    REFRESH_DIR = 'dir'

    REFRESH_TYPE = [
        {'id': REFRESH_URL, 'name': _('文件')},
        {'id': REFRESH_DIR, 'name': _('目录')},
    ]

    PRELOAD_CONDUCT = 0    # 预热进行
    PRELOAD_SUCCESS = 1    # 预热成功
    PRELOAD_FAIL = 2    # 预热失败

    PRELOAD_STATUS = [
        {'id': PRELOAD_CONDUCT, 'name': _('预加载中')},
        {'id': PRELOAD_SUCCESS, 'name': _('成功')},
        {'id': PRELOAD_FAIL, 'name': _('失败')},
    ]

    STATUS_CODE = ['200', '206', '302', '304', '403', '404', '5xx', 'other']

    STATUS_CODE_TREND = ['2xx', '3xx', '4xx', '5xx']

    @classmethod
    def get_cdn_type_name(cls, check_name):
        """cdn 加速类型"""
        type_name = ''
        for i in cls.CDN_TYPE:
            if check_name == i['check_name']:
                type_name = i['name']

        return type_name

    @classmethod
    def get_status_name(cls, status):
        """cdn 状态名称"""
        status_name = ''
        for i in cls.DOMAIN_STATUS:
            if status in i['id']:
                status_name = i['name']

        return status_name


class CertConf(object):
    """证书配置"""

    CERT_CONDUCT = 0
    CERT_SUCCESS = 1
    CERT_FAIL = 2
    CERT_TIMEOUT = 3
    CERT_DELETE = 4
    CERT_UPDATE = 5

    CERT_STATUS = [
        {'id': [CERT_UPDATE, CERT_CONDUCT], 'name': _('上传中')},
        {'id': [CERT_SUCCESS], 'name': _('正常')},
        {'id': [CERT_FAIL], 'name': _('上传失败')},
        {'id': [CERT_TIMEOUT], 'name': _('过期')},

        # {'id': CERT_DELETE, 'name': '已删除'},
    ]

    FROM_SELF = 0
    CERT_FROM = [
        {'id': FROM_SELF, 'name': _('自有证书')},
    ]

    CERT_OLD_TIME_0 = _("不提醒")
    CERT_OLD_TIME_1 = _("一个月")
    CERT_OLD_TIME_3 = _("三个月")

    # 过期提醒
    REMIND_TIME = [
        {'id': 0, 'name': CERT_OLD_TIME_0},
        {'id': 30, 'name': CERT_OLD_TIME_1},
        {'id': 3 * 30, 'name': CERT_OLD_TIME_3},
    ]

    OPT_SENDING = _('下发中')
    OPT_SEND_SUCC = _('成功')
    OPT_SEND_FAIL = _('失败')

    OPT_SEND_STATUS = [
        {'id': 0, 'name': OPT_SENDING},
        {'id': 1, 'name': OPT_SEND_SUCC},
        {'id': 2, 'name': OPT_SEND_FAIL}
    ]

    @staticmethod
    def cert_from_name(from_id):
        """来源名称"""
        name = ''
        for i in CertConf.CERT_FROM:
            if from_id == i['id']:
                name = i['name']
                break
        return name

    @staticmethod
    def cert_status_name(status_id):
        """状态名称"""
        name = ''
        for i in CertConf.CERT_STATUS:
            if status_id == i['id']:
                name = i['name']
                break
        return name




class APIUrl(object):
    """API通信"""

    PROTOCOL = 'http'

    HOST = settings.API_URL

    REQUEST_URL = {
        # user
        'create_user': '/base/internal/create_user/',
        'update_user': '/base/internal/update_user/',
        'user_open_api': '/base/internal/set_secret_key/',
        'set_api_status': '/base/internal/set_api_status/',
        'set_api_remove': '/base/internal/set_api_remove/',
        'user_query': '/base/internal/user_query/',
        'user_binding_cms': '/base/internal/user_binding_cms/',
        'user_relieve_cms_binding': '/base/internal/user_relieve_cms_binding/',
        'binding_user_contract': '/base/internal/binding_user_contract/',
        'relieve_user_contract': '/base/internal/relieve_user_contract/',
        'ssl_cert_create_or_edit': '/base/internal/ssl_cert_create_or_edit/',
        'ssl_cert_delete': '/base/internal/ssl_cert_delete/',
        'ssl_cert_query': '/base/internal/ssl_cert_query/',
        'ssl_cert_detail': '/base/internal/ssl_cert_detail/',


        # cdn domain
        'domain_query': '/base/internal/domain_query/',
        'domain_create': '/base/internal/domain_create/',
        'domain_cc_conf': '/base/internal/domain_cc_conf/',

        # waf
        'get_waf_default_rule': '/waf/default_rule_list/',
        'get_waf_self_rule': '/waf/self_rule_list/',
        'get_waf_base_info': '/waf/current_modes/',
        'set_defense_mode': '/waf/set_defense_mode/',
        'reset_default_rule': '/waf/reset_default_waf/',
        'enable_default_rule': '/waf/enable_default_rule/',
        'enable_self_rule': '/waf/enable_self_rule/',
        'waf_defense_statistics': '/waf/statistics/',
        'waf_log_list': '/waf/log_list/',
        'waf_log_detail': '/waf/log_detail/',
        'check_waf_status': '/waf/check_status/',
        'waf_binding': '/sec/internal/waf_binding/',
        'sync_domain_waf_conf': '/waf/show_info/',
        'domain_waf_set_cdn': '/sec/internal/waf_set_cdn/',
        'domain_waf_opt_waf': '/waf/record_defense/',
        'set_domain_waf_conf': '/waf/modify_info/',
        'waf_cert_upload': '/waf/cert_up/',
        'whetherBind': '/waf/tellWhetherBind/',
        'waf_create': '/sec/internal/waf_create',
        'domain_del_waf': '/waf/delete_record',
        'get_domain_status': '/waf/get_domain_status',

        # cdn
        'cdn_domain_create': '/cdn/internal/cdn/create_domain/',
        'cdn_domain_edit': '/cdn/internal/cdn/edit_domain/',
        'cdn_domain_query': '/cdn/internal/cdn/query_domain/',
        'cdn_domain_flux': '/cdn/internal/cdn/domain_flux/',
        'cdn_domain_flux_batch': '/cdn/internal/cdn/domain_flux_batch/',
        'cdn_domain_request': '/cdn/internal/cdn/domain_request/',
        'cdn_domain_status_code': '/cdn/internal/cdn/domain_status_code/',

        'cdn_domain_status_code_batch': '/cdn/internal/cdn/domain_status_code_batch/',
        'cdn_domain_sync_conf': '/cdn/internal/cdn/domain_sync_conf/',
        'cdn_domain_log': '/cdn/internal/cdn/domain_log/',
        'cdn_domain_refresh': '/cdn/internal/cdn/domain_refresh/',
        'cdn_domain_refresh_status':  '/cdn/internal/cdn/domain_refresh_status/',
        'cdn_domain_preload': '/cdn/internal/cdn/domain_preload/',
        'cdn_domain_preload_status': '/cdn/internal/cdn/domain_preload_status/',
        'cdn_domain_disable': '/cdn/internal/cdn/disable_domain/',
        'cdn_domain_active': '/cdn/internal/cdn/active_domain/',

        'test': '/base/internal/test/sf/'
    }

    @classmethod
    def post_link(cls, request_name, body):
        """通信api"""

        headers = {
            "content-type": "application/json"
        }

        data = json.dumps(body)

        url = '%s://%s%s' % (
            cls.PROTOCOL, cls.HOST, cls.REQUEST_URL[request_name])

        try:
            print(url)
            res = requests.post(url, data=data, headers=headers)
            res = res.json()
        except Exception as e:
            print(e)
            res = {}

        return res

    @classmethod
    def get_link(cls, request_name):
        """通信api"""

        headers = {
            "content-type": "application/json"
        }

        url = '%s://%s%s' % (
            cls.PROTOCOL, cls.HOST, cls.REQUEST_URL[request_name])

        try:
            res = requests.get(url, headers=headers)
            res = res.json()
        except Exception as e:
            print(e)
            res = {}

        return res

    @classmethod
    async def doPostAio(cls, request_name, body):
    # async def doPostAio(cls, request_name, body, connect_timeout=180, response_timeout=120):
        url = f'http://{cls.HOST}{cls.REQUEST_URL[request_name]}'
        conn = aiohttp.TCPConnector(limit=100) # amount of connections simultaneously limit default: 100;no limitation: 0
        # timeout = aiohttp.ClientTimeout(sock_connect=connect_timeout, sock_read=response_timeout)
        async with aiohttp.ClientSession(connector=conn) as session:
        # async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
            async with session.post(url, json=body) as response:
                r = await response.text()
                response.close()
                return r
                # return await response.text()
