/*
 Navicat Premium Data Transfer

 Source Server         : myMac
 Source Server Type    : MySQL
 Source Server Version : 50538
 Source Host           : localhost
 Source Database       : weco

 Target Server Type    : MySQL
 Target Server Version : 50538
 File Encoding         : utf-8

 Date: 09/02/2015 10:23:41 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `activity`
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `me` varchar(255) NOT NULL,
  `other` varchar(255) NOT NULL,
  `otherNickname` varchar(255) NOT NULL,
  `ideaId` int(11) NOT NULL,
  `ideaTitle` varchar(255) NOT NULL,
  `comment` text NOT NULL,
  `activityType` int(11) NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `checked` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `activity`
-- ----------------------------
BEGIN;
INSERT INTO `activity` VALUES ('1', 'Honlan', 'Honlan', '伦大锤', '8', '真是屌', '心好累', '3', '1440560857', '1'), ('2', 'Test', 'Honlan', '伦大锤', '0', '', '', '1', '1440605263', '0'), ('3', 'Honlan', '12345', '12345', '20', 'dasds', '', '2', '1440731838', '0'), ('4', 'Honlan', '12345', '12345', '20', 'dasds', '', '2', '1440731841', '0'), ('5', 'Honlan', '12345', '12345', '0', '', '', '1', '1440732046', '0');
COMMIT;

-- ----------------------------
--  Table structure for `attachment`
-- ----------------------------
DROP TABLE IF EXISTS `attachment`;
CREATE TABLE `attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ideaId` int(11) NOT NULL,
  `fileType` int(11) NOT NULL DEFAULT '0',
  `url` text NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `attachment`
-- ----------------------------
BEGIN;
INSERT INTO `attachment` VALUES ('14', '3', '0', '这是第二个创意，简直是屌', '1440492735', 'Honlan'), ('15', '4', '0', '第三个创意', '1440492848', 'Honlan'), ('16', '5', '0', '好的很', '1440493692', 'Honlan'), ('17', '6', '0', '不懂', '1440493716', 'Honlan'), ('19', '7', '0', '啊啊啊啊我确实有点蛋疼\n有点难过\n啊啊啊啊啊\n啊啊啊啊啊啊\n', '1440550839', 'Honlan'), ('20', '7', '0', '我有点烦，你觉得呢？\n真的是太奇怪了\n', '1440550901', 'Honlan'), ('21', '7', '0', '真的是烦死了\n', '1440550999', 'Honlan'), ('22', '8', '0', '心好累', '1440560682', 'Honlan'), ('23', '9', '0', '真的是特别恶心\n', '1440561116', 'Honlan'), ('24', '19', '0', '第一段话', '1440597705', 'Honlan'), ('25', '20', '0', '无啦啦', '1440597852', 'Honlan'), ('26', '20', '0', '第一段话', '1440600254', 'Honlan'), ('27', '21', '0', ' 第一段话', '1440600333', 'Honlan'), ('28', '22', '0', '第一段话', '1440600361', 'Honlan'), ('29', '23', '0', '第一句话', '1440600485', 'Honlan'), ('30', '24', '0', '第一句话', '1440600522', 'Honlan'), ('31', '24', '0', '第二句话', '1440600527', 'Honlan'), ('32', '24', '0', '第三句话\n真是好\n\n   空格\n\n回车', '1440600541', 'Honlan'), ('42', '27', '0', '啊啊啊啊', '1440602249', 'Honlan'), ('43', '27', '0', '继续说话', '1440602254', 'Honlan'), ('44', '27', '1', '/static/uploads/img/2015082623_FAB2335EC4.jpg', '1440602261', 'Honlan'), ('45', '28', '0', 'asdasd', '1440602565', 'Honlan'), ('46', '28', '0', 'asdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfafasdasfaf', '1440602572', 'Honlan'), ('47', '28', '1', '/static/uploads/img/2015082623_19573B1999.jpg', '1440602579', 'Honlan'), ('48', '29', '0', '我说一句话', '1440602757', 'Honlan'), ('49', '29', '1', '/static/uploads/img/2015082623_AC833171EA.jpg', '1440602762', 'Honlan'), ('50', '29', '1', '/static/uploads/img/2015082623_0D2F3CAAF5.jpg', '1440602771', 'Honlan'), ('51', '29', '1', '/static/uploads/img/2015082623_FBBE9DFE77.jpg', '1440602783', 'Honlan'), ('52', '29', '1', '/static/uploads/img/2015082623_7A2C7EFAC0.jpg', '1440602792', 'Honlan'), ('53', '30', '1', '/static/uploads/img/2015082623_1A44D58AC1.jpg', '1440602869', 'Honlan'), ('54', '30', '0', 'asdadasa', '1440602882', 'Honlan'), ('55', '31', '1', '/static/uploads/img/2015082623_5336A662CA.jpg', '1440602935', 'Honlan'), ('56', '31', '0', '不错不错', '1440602941', 'Honlan'), ('57', '32', '1', '/static/uploads/img/2015082623_DEEF7EE4BA.jpg', '1440603246', 'Honlan'), ('58', '32', '1', '/static/uploads/img/2015082623_778C7BABCF.jpg', '1440603268', 'Honlan'), ('59', '33', '1', '/static/uploads/img/2015082623_95DAF9F435.jpg', '1440603515', 'Honlan'), ('62', '35', '0', '好的', '1440603720', 'Honlan'), ('63', '36', '0', '阿萨德大', '1440603760', 'Honlan'), ('64', '41', '1', '/static/uploads/img/2015082814_1B09F15FB1.jpg', '1440743143', '12345'), ('65', '42', '0', '我来说话', '1440743284', '12345'), ('66', '43', '0', '这下可以了', '1440743388', '12345'), ('67', '43', '1', '/static/uploads/img/2015082814_A8FCD75080.jpg', '1440743392', '12345'), ('68', '43', '1', '/static/uploads/img/2015082814_092D7BECD7.jpg', '1440743399', '12345'), ('69', '44', '0', 'wish 嗯噩梦哈斯和 i', '1440744173', '12345'), ('70', '44', '1', '/static/uploads/img/2015082814_DAC085FA9C.jpg', '1440744179', '12345');
COMMIT;

-- ----------------------------
--  Table structure for `chat`
-- ----------------------------
DROP TABLE IF EXISTS `chat`;
CREATE TABLE `chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(255) NOT NULL,
  `sourceNickname` varchar(255) NOT NULL,
  `target` varchar(255) NOT NULL,
  `targetNickname` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `checked` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `chat`
-- ----------------------------
BEGIN;
INSERT INTO `chat` VALUES ('1', 'Honlan', '伦大锤', 'None', 'None', '这不就可以了么', '1440463926', '1');
COMMIT;

-- ----------------------------
--  Table structure for `comment`
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `portrait` varchar(255) NOT NULL DEFAULT '/static/img/user.png',
  `ideaId` int(11) NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `praise` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `comment`
-- ----------------------------
BEGIN;
INSERT INTO `comment` VALUES ('1', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '8', '1440560857', '心好累', '1');
COMMIT;

-- ----------------------------
--  Table structure for `idea`
-- ----------------------------
DROP TABLE IF EXISTS `idea`;
CREATE TABLE `idea` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `tags` text NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `portrait` varchar(255) NOT NULL DEFAULT '/static/img/user.png',
  `praise` int(11) NOT NULL DEFAULT '0',
  `readCount` int(11) NOT NULL DEFAULT '0',
  `lastUpdate` varchar(255) NOT NULL,
  `thumbnail` varchar(255) NOT NULL DEFAULT '/static/img/idea.jpg',
  `feature` varchar(255) NOT NULL DEFAULT '/static/img/idea.jpg',
  `commentCount` int(11) NOT NULL DEFAULT '0',
  `published` int(1) NOT NULL DEFAULT '0',
  `locked` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `idea`
-- ----------------------------
BEGIN;
INSERT INTO `idea` VALUES ('12', '标题', '社会创新', '阿萨德', '1440595193', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/uploads/img/2015082621_4B6528E617.jpg', '/static/uploads/img/2015082621_4B6528E617_thumb.jpg', '0', '1', '0'), ('13', '萨达', '社会创新', '呀呀呀', '1440595814', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('14', '标题', '社会创新', '呀呀呀', '1440596160', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('15', '阿萨德', '社会创新', '啊啊啊', '1440596454', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('16', 'asd', '社会创新', '呀呀呀', '1440596616', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('17', '标题啊', '社会创新', '我帅 阿萨德', '1440597568', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/uploads/img/2015082621_C812275F54.jpg', '/static/uploads/img/2015082621_C812275F54_thumb.jpg', '0', '0', '0'), ('18', 'kkkk', '社会创新', '啊啊啊', '1440597659', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('19', '萨达', '社会创新', '阿萨德', '1440597696', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('20', 'dasds', '社会创新', '呀呀呀', '1440597843', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('21', 'asd', '社会创新', '啊啊啊', '1440600325', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('22', 'asd', '社会创新', '呀呀呀', '1440600357', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('23', 'asdasd', '社会创新', '啊啊啊', '1440600480', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('24', '大三大四的', '社会创新', '呀呀呀', '1440600517', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('25', '阿萨德撒的', '社会创新', '啊啊啊', '1440600868', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('26', '测试啊啊啊', '社会创新', '呀呀呀', '1440602022', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('27', 'rtert', '社会创新', '啊啊啊', '1440602244', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('28', 'asdasd', '社会创新', '啊啊啊', '1440602561', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('29', '大大的', '社会创新', '呀呀呀', '1440602752', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('30', 'wqewe', '社会创新', '阿萨德', '1440602860', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('31', '哇哈哈', '社会创新', '呀呀呀', '1440602925', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('32', '可以删除附件了！', '社会创新', '啊啊啊', '1440603181', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('33', 'adsdasd', '社会创新', '呀呀呀', '1440603506', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('34', 'pppp', '社会创新', '奋斗', '1440603585', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('35', '确实不知道为什么', '社会创新', '呀呀呀', '1440603716', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('36', '大萨达', '社会创新', '啊啊啊', '1440603757', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('37', '现在总可以了吧', '社会创新', '耶 呀呀呀', '1440603813', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('38', '好的很', '社会创新', '好的很', '1440603920', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('39', '蛋疼死了', '社会创新', '哇哈哈', '1440603954', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '0', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '0', '0'), ('40', '看来可以隐藏了', '社会创新', '啊啊啊', '1440604114', 'Honlan', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0'), ('41', 'asdsad', '社会创新', '呀呀呀', '1440743128', '12345', '12345', '/static/img/user.png', '0', '1', '', '/static/uploads/img/2015082814_FB6E21138C.jpg', '/static/uploads/img/2015082814_FB6E21138C_thumb.jpg', '0', '1', '0'), ('42', '这次应该可以了', '社会创新', '阿萨德', '1440743266', '12345', '12345', '/static/img/user.png', '0', '1', '', '/static/uploads/img/2015082814_41A24E3928.jpg', '/static/uploads/img/2015082814_41A24E3928_thumb.jpg', '0', '1', '0'), ('43', '现在总好了呐', '社会创新', '阿萨德', '1440743328', '12345', '12345', '/static/img/user.png', '0', '1', '', '/static/uploads/img/2015082814_40B5D41936.jpg', '/static/uploads/img/2015082814_40B5D41936_thumb.jpg', '0', '1', '0'), ('44', '啊实打实大', '社会创新', '啊啊啊', '1440744167', '12345', '12345', '/static/img/user.png', '0', '1', '', '/static/img/idea.jpg', '/static/img/idea.jpg', '0', '1', '0');
COMMIT;

-- ----------------------------
--  Table structure for `ideaTagStat`
-- ----------------------------
DROP TABLE IF EXISTS `ideaTagStat`;
CREATE TABLE `ideaTagStat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `ideaTagStat`
-- ----------------------------
BEGIN;
INSERT INTO `ideaTagStat` VALUES ('1', '测试', '艺术', '26'), ('2', '第一个', '艺术', '1'), ('3', '哈哈哈', '艺术', '1'), ('4', '啊啊啊', '艺术', '2'), ('5', '是屌啊', '艺术', '1'), ('6', '为啥', '艺术', '5'), ('7', '啊啊啊', '社会创新', '16'), ('8', '一一一', '社会创新', '1'), ('9', '呀呀呀', '社会创新', '16'), ('10', '阿萨德', '社会创新', '7'), ('11', '发达省份', '社会创新', '1'), ('12', '奋斗', '社会创新', '2'), ('13', '问题', '社会创新', '1'), ('14', '我帅', '社会创新', '1'), ('15', '耶', '社会创新', '1'), ('16', '好的很', '社会创新', '1'), ('17', '哇哈哈', '社会创新', '1');
COMMIT;

-- ----------------------------
--  Table structure for `search`
-- ----------------------------
DROP TABLE IF EXISTS `search`;
CREATE TABLE `search` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `target` varchar(8) NOT NULL DEFAULT 'idea',
  `keyword` varchar(255) NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `search`
-- ----------------------------
BEGIN;
INSERT INTO `search` VALUES ('1', '', 'user', '', '1440333918'), ('2', '', 'user', '', '1440333919'), ('3', '', 'user', '', '1440333988'), ('4', '', 'user', '', '1440333989'), ('5', '', 'user', '', '1440333998'), ('6', '', 'user', '', '1440333998'), ('7', '', 'user', '', '1440334040'), ('8', '', 'user', '', '1440334053'), ('9', '', 'user', '', '1440334054'), ('10', '', 'user', '', '1440334063'), ('11', '', 'user', '', '1440334064'), ('12', '', 'user', '', '1440334078'), ('13', '', 'user', '', '1440334079'), ('14', '', 'user', '', '1440334088'), ('15', '', 'user', '', '1440334089'), ('16', '', 'user', '', '1440334729'), ('17', '', 'user', '', '1440334730'), ('18', '', 'user', '', '1440334736'), ('19', '', 'user', '', '1440334736'), ('20', '', 'user', '', '1440335506'), ('21', '', 'user', '', '1440335506'), ('22', '', 'user', '', '1440335567'), ('23', '', 'user', '', '1440335567'), ('24', '', 'user', '', '1440335625'), ('25', '', 'user', '', '1440335625'), ('26', 'Honlan', 'idea', '智慧城市', '1440374429'), ('27', 'Honlan', 'idea', '智慧城市', '1440374430'), ('28', 'Honlan', 'idea', '天才', '1440425190'), ('29', 'Honlan', 'idea', '天才', '1440425191'), ('30', 'Honlan', 'idea', '天才', '1440425232'), ('31', 'Honlan', 'idea', '天才', '1440425234'), ('32', 'Honlan', 'idea', '天才', '1440425280'), ('33', 'Honlan', 'idea', '天才', '1440425281'), ('34', '', 'user', '', '1440472442'), ('35', '', 'user', '', '1440472443'), ('36', 'wahaha', 'user', '', '1440492451'), ('37', 'wahaha', 'user', '', '1440492451'), ('38', 'Honlan', 'user', '', '1440493355'), ('39', 'Honlan', 'user', '', '1440493355'), ('40', 'Honlan', 'user', 'Honlan', '1440558915'), ('41', 'Honlan', 'user', 'Honlan', '1440558915'), ('42', 'Honlan', 'user', 'Honlan', '1440558951'), ('43', 'Honlan', 'user', 'Honlan', '1440558952'), ('44', 'Honlan', 'user', 'Honlan', '1440605159'), ('45', 'Honlan', 'user', 'Honlan', '1440605159'), ('46', 'Honlan', 'user', 'Honlan', '1440605163'), ('47', 'Honlan', 'user', 'Honlan', '1440605163'), ('48', 'Honlan', 'user', '伦大锤', '1440605175'), ('49', 'Honlan', 'user', '伦大锤', '1440605176'), ('50', 'Honlan', 'idea', '啦啦啦', '1440605204'), ('51', 'Honlan', 'idea', '啦啦啦', '1440605204'), ('52', 'Honlan', 'idea', '呀呀呀', '1440605210'), ('53', 'Honlan', 'idea', '呀呀呀', '1440605210'), ('54', 'Honlan', 'user', '', '1440605237'), ('55', 'Honlan', 'user', '', '1440605237'), ('56', 'Honlan', 'user', '', '1440605256'), ('57', 'Honlan', 'user', '', '1440605256'), ('58', '12345', 'idea', '智慧城市', '1440730859'), ('59', '12345', 'idea', '智慧城市', '1440730859'), ('60', '12345', 'user', 'Honlan', '1440730861'), ('61', '12345', 'user', 'Honlan', '1440730861'), ('62', '12345', 'idea', '天才', '1440730866'), ('63', '12345', 'idea', '天才', '1440730866'), ('64', '12345', 'user', '伦大锤', '1440730868'), ('65', '12345', 'user', '伦大锤', '1440730868'), ('66', '12345', 'user', '伦大锤', '1440730934'), ('67', '12345', 'user', '伦大锤', '1440730993'), ('68', '12345', 'user', '伦大锤', '1440730993'), ('69', '12345', 'user', '伦大锤', '1440730995'), ('70', 'Honlan', 'idea', '我靠', '1440988277'), ('71', 'Honlan', 'idea', '我靠', '1440988277');
COMMIT;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `portrait` varchar(255) NOT NULL DEFAULT '/static/img/user.png',
  `tags` text NOT NULL,
  `description` text NOT NULL,
  `gender` int(1) NOT NULL DEFAULT '1',
  `wechat` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `hobby` varchar(255) NOT NULL,
  `ideas` longtext NOT NULL,
  `followIdeas` longtext NOT NULL,
  `fans` longtext NOT NULL,
  `followUsers` longtext NOT NULL,
  `lastActive` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `TTL` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'None', '493722771@qq.com', 'D3E0D13A2573A4B765C3A4CC2CEA3BA8', 'None', '/static/img/user.png', '', '', '1', '', '', '', '', '', '', '', '1440463947', '7561601B63BDC2B6CB4E4A17EB6F836A', '100'), ('2', 'Honlan', 'zhanghonglun@sjtu.edu.cn', 'D3E0D13A2573A4B765C3A4CC2CEA3BA8', '伦大锤', '/static/uploads/img/2015082700_65470199F7.jpg', '啦啦啦', '是时候展现真正的技术了', '1', 'honlann', '上海', '吃饭啊睡觉啊', '10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40', '', '12345', 'Test', '1441159129', '111418D2AE20690107525DEDA21EE0AF', '100'), ('3', 'Test', 'qweqwew@qq.com', '202CB962AC59075B964B07152D234B70', 'Test', '/static/uploads/img/2015082509_166C7C18FF.jpg', '啦啦啦', '我是一只乖熊熊', '0', 'Bear', '上海 上海市', '吃饭，睡觉，打豆豆，吃', '', '', 'Honlan', '', '1440464160', '7A530CBE3DD3D81AB07ED4EED583F359', '100'), ('4', 'wahaha', '1231@qq.com', '202CB962AC59075B964B07152D234B70', 'wahaha', '/static/img/user.png', '', '', '1', '', '', '', '', '', '', '', '1440557432', '38456E028923EA44D77E40EADE8C6FBF', '100'), ('5', '12345', '12345@qq.com', '202CB962AC59075B964B07152D234B70', '12345', '/static/img/user.png', '', '', '1', '', '', '', '41,42,43,44', '20', '', 'Honlan', '1440744720', '6724C85865C3C420BB59130889DC9CB2', '100');
COMMIT;

-- ----------------------------
--  Table structure for `userTagStat`
-- ----------------------------
DROP TABLE IF EXISTS `userTagStat`;
CREATE TABLE `userTagStat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) NOT NULL,
  `gender` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `userTagStat`
-- ----------------------------
BEGIN;
INSERT INTO `userTagStat` VALUES ('1', '啦啦啦', '0', '3'), ('2', '啦啦啦', '1', '10');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
