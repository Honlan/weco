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

 Date: 08/23/2015 16:57:50 PM
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `commentCount` int(11) NOT NULL DEFAULT '0',
  `locked` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  `ideas` longtext NOT NULL,
  `followIdeas` longtext NOT NULL,
  `fans` longtext NOT NULL,
  `followUsers` longtext NOT NULL,
  `lastActive` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `TTL` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'None', '493722771@qq.com', 'D3E0D13A2573A4B765C3A4CC2CEA3BA8', 'None', '/static/img/user.png', '', '', '1', '', '', '', '', '', '1440319952', 'F65FC5C6B4290CC853B4E2D9B5784A88', '100'), ('2', 'Honlan', 'zhanghonglun@sjtu.edu.cn', 'D3E0D13A2573A4B765C3A4CC2CEA3BA8', 'Honlan', '/static/img/user.png', '', '', '1', '', '', '', '', '', '1440320164', 'BFC9244ADD025EFC1C7C7F661E2238C7', '100');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
