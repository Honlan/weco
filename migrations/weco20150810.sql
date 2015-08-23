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

 Date: 08/10/2015 11:19:00 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `comment`
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `ideaId` int(11) NOT NULL,
  `timestamp` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `praise` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `comment`
-- ----------------------------
BEGIN;
INSERT INTO `comment` VALUES ('2', 'honlan', '伦大锤就是我', '13', '1438760310', '这才是第一条评论', '0'), ('3', 'honlan', '伦大锤就是我', '13', '1438760400', '我再来写一条评论好了', '0'), ('4', 'honlan', '伦大锤就是我', '13', '1438761588', '这是我的第三条评论', '0'), ('5', 'honlan', '伦大锤就是我', '12', '1438762117', '这是我自己发的评论', '1'), ('6', 'honlan', '伦大锤就是我', '9', '1438823114', '我来抢个沙发', '1'), ('7', 'bibi2', 'bibi2', '9', '1438823637', '第二条评论', '0'), ('8', 'bibi2', 'bibi2', '13', '1438870193', '评论呀评论', '1'), ('9', 'bibi2', 'bibi2', '13', '1438870234', '简直不能忍', '0'), ('10', 'bibi2', 'bibi2', '13', '1438934032', '以前的评论不算数原来', '1'), ('11', 'bibi2', 'bibi2', '13', '1439021383', '我怎么不能评论了？', '0'), ('12', 'bibi2', 'bibi2', '13', '1439021410', '什么鬼', '1'), ('13', 'honlan', '伦大锤就是我', '12', '1439171853', '评论', '0');
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
  `praise` int(11) NOT NULL DEFAULT '0',
  `readCount` int(11) NOT NULL DEFAULT '0',
  `lastUpdate` varchar(255) NOT NULL,
  `thumbnail` varchar(255) NOT NULL DEFAULT '/static/img/idea.jpg',
  `commentCount` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `idea`
-- ----------------------------
BEGIN;
INSERT INTO `idea` VALUES ('9', 'Honlan的第二个创意', '坑爹', '逗比,好玩,测试', '1438444098', 'honlan', '1', '1', '1438820810', '/static/img/idea.jpg', '0'), ('10', '第10个', '科技', '逗比,好玩,测试,啦啦啦', '1438444188', 'honlan', '0', '1', '1438525397', '/static/img/idea.jpg', '0'), ('11', 'Honlan的很多创意', '艺术', '逗比,好玩,测试', '1438447868', 'honlan', '0', '1', '1438591217', '/static/img/idea.jpg', '0'), ('12', 'zhl的创意', '艺术', 'zhl', '1438571368', 'zhl', '1', '1', '', '/static/img/idea.jpg', '1'), ('13', '乖比比你懂的', '艺术真好', '比比的创意', '1438596056', 'bibi2', '0', '1', '1439170484', '/static/img/idea.jpg', '5'), ('14', '测试', 'nice', '看来是成功了', '1439172181', 'honlan', '0', '1', '1439176345', '/static/uploads/img/20150810_D18BC3FF49_21.jpg', '0');
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
  `portrait` text NOT NULL,
  `tags` text NOT NULL,
  `description` text NOT NULL,
  `gender` int(1) NOT NULL DEFAULT '1',
  `wechat` varchar(255) NOT NULL,
  `ideas` text NOT NULL,
  `followIdeas` text NOT NULL,
  `fans` text NOT NULL,
  `followUsers` text NOT NULL,
  `lastActive` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `TTL` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'honlan', 'aaa493722771@qq.com', '202CB962AC59075B964B07152D234B70', '伦大锤就是我', '', '啦啦啦,程序员,设计师,学生,90后,创业者,技术宅', '笑死生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。', '0', 'Honlann111', '9,10,11,14', '13', 'bibi,zhl,bibi2', 'bibi', '1439172363', '7CD895ED5A70E3AFA0A33CBA57EE9B66', '99'), ('2', 'zhl', '493722771@qq.com', '202CB962AC59075B964B07152D234B70', 'zhl', '', '', '', '1', '', '12', '11', 'bibi', 'honlan', '1438587631', '77ABBAF50A111B3B61977BEE4F0D0861', '98'), ('3', 'bibi', 'asdasdasfa@qq.com', '202CB962AC59075B964B07152D234B70', 'bibi', '', '', '', '1', '', '', '12,11,10', 'honlan,bibi2', 'zhl,honlan', '1439171661', 'BC1EF44D89817DF599025BC11631BBB4', '100'), ('4', 'bibi2', 'adsaafa@qq.com', '202CB962AC59075B964B07152D234B70', 'bibi2', '', '我叫乖比比', '你叫臭大宝', '0', 'guaibibi', '13', '', '', 'honlan,bibi', '1439172248', '7F441B1F87E303538109BC1D41B89AD1', '100');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
