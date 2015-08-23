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

 Date: 08/03/2015 17:26:46 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `idea`
-- ----------------------------
BEGIN;
INSERT INTO `idea` VALUES ('9', 'Honlan的第二个创意', '坑爹', '逗比,好玩,测试', '1438444098', 'honlan', '0', '0', '1438588646'), ('10', '第10个', '科技', '逗比,好玩,测试,啦啦啦', '1438444188', 'honlan', '0', '0', '1438525397'), ('11', 'Honlan的很多创意', '艺术', '逗比,好玩,测试', '1438447868', 'honlan', '0', '0', '1438591217'), ('12', 'zhl的创意', '艺术', 'zhl', '1438571368', 'zhl', '0', '0', '');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'honlan', 'aaa493722771@qq.com', '202CB962AC59075B964B07152D234B70', '伦大锤就是我', '', '啦啦啦,程序员,设计师,学生,90后,创业者,技术宅', '笑死生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。生命不息，奋斗不止。', '0', 'Honlann111', '9,10,11', '', 'bibi,zhl', '', '1438593748', '2C5464CE233F7BC25AB8F5A29958837C', '100'), ('2', 'zhl', '493722771@qq.com', '202CB962AC59075B964B07152D234B70', 'zhl', '', '', '', '1', '', '12', '11', 'bibi', 'honlan', '1438587631', '77ABBAF50A111B3B61977BEE4F0D0861', '98'), ('3', 'bibi', 'asdasdasfa@qq.com', '202CB962AC59075B964B07152D234B70', 'bibi', '', '', '', '1', '', '', '12,11,10', '', 'zhl,honlan', '1438587678', '18F5372F8AD279CCDD7D5D1FB3D85F7F', '100');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
