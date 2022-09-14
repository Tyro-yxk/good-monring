# 更新说明
## 2022.09.14
1. 根据自己low的英语水平和习惯，更改了一些名字的命名格式
2. 依旧支持多个生日倒计时，但是没有兼容2022-01-01格式，只支持01-01格式（非农历）输入格式：01-01;01-02
3. 更新支持多个地址（理论无限个）*上一个版本即使不需要第二个地址，也必须输入，现在这个版本可以不输入*，可以一个写家乡，一个写工作或学习的地方，或者写异地对象的地址；输入格式：北京;淮阴区
4. 更新支持多个正数纪念（如在一起多少天，出生多少天）（理论无线个）输入时间格式：2022-01-01;2022-01-02
5. 支持输出对应地址
6. 输出农历日期（农历不支持生日），输出周几
7. 所以输入格式之间的**分号 *;* 均是英文分号**

##### 示例模板
[模板](./模板.txt)
今天是{{y_date.DATA}} {{x_date.DATA}}{{weekday.DATA}}

今日家乡{{city.DATA}}天气：{{we_city.DATA}} 

当前温度：{{te_city.DATA}} ℃ 

今日最低气温：{{lo_city.DATA}} ℃ 

今日最高气温：{{hi_city.DATA}} ℃ 

空气湿度：{{hu_city.DATA}} 

今日风向：{{wi_city.DATA}} 

空气质量：{{ai_city.DATA}} 

今日学校{{city_1.DATA}}天气：{{we_city_1.DATA}} 

当前温度：{{te_city_1.DATA}} ℃ 

今日最低气温：{{lo_city_1.DATA}} ℃ 

今日最高气温：{{hi_city_1.DATA }} ℃ 

空气湿度：{{hu_city_1.DATA}} 

今日风向：{{wi_city_1.DATA}} 

空气质量：{{ai_city_1.DATA}} 

我已经出生{{start.DATA}}天 

已经相识{{start_1.DATA}}天

距离你的生日还有{{rec.DATA}} 天 

距离考试还有{{rec_1.DATA}}天

{{words.DATA}} 

--科科 ！

### 模板说明
{{y_date.DATA}} 阳历

{{x_date.DATA}} 农历

{{weekday.DATA}} 星期（如：周三）

{{city.DATA}} 城市 （输出格式：**北京**  ***四川-成都*** **江苏-淮安-淮阴区**  三种）

{{we_city.DATA}} 天气

{{te_city.DATA}} 当前温度

{{lo_city.DATA}} 最低温度

{{hi_city.DATA}}最高温度

{{hu_city.DATA}}空气湿度

{{wi_city.DATA}}风向

{{ai_city.DATA}} 空气质量

{{start.DATA}}正数纪念（如出生多少天，相识多少天）

{{rec.DATA}}倒数多少天（如生日还有多少天，xx纪念日还有多少天）

{{words.DATA}} 每日一句彩虹屁

**模板中的中文可以自定义，{{}}中的英文不能修改，数字可以递增（两个出现数字1,三个就出现2）**

**温度没输出°C使用者自定义更高（如：今日温度xx~xx°C）**

**v信字数限制，如果出现未显示完全，可删除一些对自己无用的**

原作者的最新[更新](./auth_UPGRADE.md)，我在其基础上更新
## 2022.08.22

1. 增加天气范围（最高温、最低温）
2. 支持多个接收人
3. 所有字段都是彩色的
4. 增加多个地址

示例模板：

今天是 {{ date.DATA }}

今天天气：{{weather.DATA }}

当前温度：{{ temperature.DATA }}

低温：{{ lowest.DATA }}

最高温：{{ highest.DATA }}

我们已经相恋 {{ love_days.DATA }} 天啦

距离你的生日还有：{{ birthday_left.DATA }} 天

{{ words.DATA }}
