/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2019-02-14 12:55:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'admin', 'pbkdf2:sha256:50000$6HfC5458$21ce960b21eb2d9120ca566ace313748343037238c698721c0cab6d406302fe5', '0', '11', '2019-01-24 14:33:14');
INSERT INTO `admin` VALUES ('2', 'abc123', 'pbkdf2:sha256:50000$FtSOQqGr$571c2ba52f6521560d361065d2e10844026f759ed9e23e888da74e5076c43031', '1', '8', '2019-02-01 09:26:20');
INSERT INTO `admin` VALUES ('3', 'def123', 'pbkdf2:sha256:50000$MKk2UXkj$5494aa2ee6023f8f8c97ef6c10e2fbe8cac454bc57a20b01082cb5d7d31cee4a', '1', '10', '2019-02-01 09:27:35');
INSERT INTO `admin` VALUES ('4', '超级管理员', 'pbkdf2:sha256:50000$GLbjrcWb$2220b5b20f72bf71fbd8b218690d910ef3cd14b911475219aad01e4623fb34c1', '0', '11', '2019-02-01 09:51:59');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES ('1', '1', '127.0.0.1', '2019-01-28 11:09:20');
INSERT INTO `adminlog` VALUES ('2', '1', '127.0.0.1', '2019-01-28 11:09:35');
INSERT INTO `adminlog` VALUES ('3', '1', '127.0.0.1', '2019-01-28 11:56:45');
INSERT INTO `adminlog` VALUES ('4', '1', '127.0.0.1', '2019-01-28 13:27:04');
INSERT INTO `adminlog` VALUES ('5', '1', '127.0.0.1', '2019-01-28 19:13:03');
INSERT INTO `adminlog` VALUES ('6', '1', '127.0.0.1', '2019-01-28 19:13:52');
INSERT INTO `adminlog` VALUES ('7', '1', '127.0.0.1', '2019-01-28 19:15:18');
INSERT INTO `adminlog` VALUES ('8', '1', '127.0.0.1', '2019-01-31 12:25:49');
INSERT INTO `adminlog` VALUES ('9', '1', '127.0.0.1', '2019-02-01 09:44:20');
INSERT INTO `adminlog` VALUES ('10', '2', '127.0.0.1', '2019-02-01 10:30:16');
INSERT INTO `adminlog` VALUES ('11', '1', '127.0.0.1', '2019-02-01 10:31:00');
INSERT INTO `adminlog` VALUES ('12', '1', '127.0.0.1', '2019-02-01 12:12:20');
INSERT INTO `adminlog` VALUES ('13', '1', '127.0.0.1', '2019-02-01 12:16:58');
INSERT INTO `adminlog` VALUES ('14', '1', '127.0.0.1', '2019-02-12 11:22:56');
INSERT INTO `adminlog` VALUES ('15', '1', '127.0.0.1', '2019-02-12 11:57:02');
INSERT INTO `adminlog` VALUES ('16', '1', '127.0.0.1', '2019-02-12 20:03:24');
INSERT INTO `adminlog` VALUES ('17', '1', '127.0.0.1', '2019-02-12 20:09:40');
INSERT INTO `adminlog` VALUES ('18', '1', '127.0.0.1', '2019-02-13 09:48:44');
INSERT INTO `adminlog` VALUES ('19', '1', '127.0.0.1', '2019-02-14 11:16:44');
INSERT INTO `adminlog` VALUES ('20', '1', '127.0.0.1', '2019-02-14 11:17:13');
INSERT INTO `adminlog` VALUES ('21', '1', '127.0.0.1', '2019-02-14 11:17:24');
INSERT INTO `adminlog` VALUES ('22', '1', '127.0.0.1', '2019-02-14 11:17:40');
INSERT INTO `adminlog` VALUES ('23', '1', '127.0.0.1', '2019-02-14 11:23:17');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES ('3', '添加标签', '/admin/tag/add/', '2019-01-28 15:47:52');
INSERT INTO `auth` VALUES ('4', '编辑标签', '/admin/tag/edit/<int:id>/', '2019-01-28 15:50:09');
INSERT INTO `auth` VALUES ('5', '标签列表', '/admin/tag/list/<int:page>/', '2019-01-28 15:50:49');
INSERT INTO `auth` VALUES ('7', '删除标签', '/admin/tag/del/<int:id>/', '2019-01-28 15:51:47');
INSERT INTO `auth` VALUES ('8', '添加电影', '/admin/movie/add/', '2019-01-28 15:52:00');
INSERT INTO `auth` VALUES ('9', '电影列表', '/admin/movie/list/<int:page>/', '2019-01-28 15:52:13');
INSERT INTO `auth` VALUES ('10', '删除电影', '/admin/movie/del/<int:id>/', '2019-01-28 15:52:25');
INSERT INTO `auth` VALUES ('11', '修改电影', '/admin/movie/edit/<int:id>/', '2019-01-28 15:52:39');
INSERT INTO `auth` VALUES ('12', '编辑上映电影', '/admin/preview/add/', '2019-01-28 15:53:01');
INSERT INTO `auth` VALUES ('13', '上映预告列表', '/admin/preview/list/<int:page>/', '2019-01-28 15:53:19');
INSERT INTO `auth` VALUES ('14', '删除上映预告列表', '/admin/preview/del/<int:id>/', '2019-01-28 15:54:51');
INSERT INTO `auth` VALUES ('15', '编辑上映预告列表', '/admin/preview/edit/<int:id>/', '2019-01-28 15:55:11');
INSERT INTO `auth` VALUES ('16', '会员列表', '/admin/user/list/<int:page>/', '2019-01-28 15:55:35');
INSERT INTO `auth` VALUES ('17', '删除会员', '/admin/user/del/<int:id>/', '2019-01-28 15:58:02');
INSERT INTO `auth` VALUES ('18', '评论列表', '/admin/comment/list/<int:page>/', '2019-01-28 15:58:21');
INSERT INTO `auth` VALUES ('19', '删除评论', '/admin/comment/del/<int:id>/', '2019-01-28 15:58:33');
INSERT INTO `auth` VALUES ('20', '删除收藏', '/admin/moviecol/del/<int:id>/', '2019-01-28 15:58:48');
INSERT INTO `auth` VALUES ('21', '操作日志列表查询', '/admin/oplog/list/<int:page>/', '2019-01-28 15:59:04');
INSERT INTO `auth` VALUES ('22', '管理员日志列表查询', '/admin/adminloginlog/list/<int:page>/', '2019-01-28 15:59:30');
INSERT INTO `auth` VALUES ('23', '用户登陆日志列表查询', '/admin/userloginlog/list/<int:page>/', '2019-01-28 15:59:50');
INSERT INTO `auth` VALUES ('24', '查看会员', '/admin/user/view/<int:id>/', '2019-02-01 10:38:54');
INSERT INTO `auth` VALUES ('27', '收藏列表', '/admin/moviecol/list/<int:page>/', '2019-02-01 12:10:47');
INSERT INTO `auth` VALUES ('28', '添加管理员', '/admin/admin/add/', '2019-02-01 12:15:23');
INSERT INTO `auth` VALUES ('29', '管理员列表', '/admin/admin/list/<int:page>/', '2019-02-01 12:15:45');
INSERT INTO `auth` VALUES ('30', '添加权限', '/admin/auth/add/', '2019-02-01 12:18:39');
INSERT INTO `auth` VALUES ('31', '权限列表', '/admin/auth/list/<int:page>/', '2019-02-01 12:18:58');
INSERT INTO `auth` VALUES ('32', '删除权限', '/admin/auth/del/<int:id>/', '2019-02-01 12:19:10');
INSERT INTO `auth` VALUES ('33', '编辑权限', '/admin/auth/edit/<int:id>', '2019-02-01 12:19:21');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES ('32', '难看', '25', '5', '2019-01-26 14:10:36');
INSERT INTO `comment` VALUES ('33', '无聊', '25', '3', '2019-01-26 14:10:36');
INSERT INTO `comment` VALUES ('34', '乏味', '26', '7', '2019-01-26 14:10:36');
INSERT INTO `comment` VALUES ('35', '无感', '26', '8', '2019-01-26 14:10:36');
INSERT INTO `comment` VALUES ('36', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0005.gif\"/>好看!</p>', '38', '12', '2019-02-13 09:43:48');
INSERT INTO `comment` VALUES ('37', '<p><img src=\"http://img.baidu.com/hi/babycat/C_0001.gif\"/>超级好看</p>', '38', '12', '2019-02-13 09:44:37');
INSERT INTO `comment` VALUES ('38', '<p><img src=\"http://img.baidu.com/hi/babycat/C_0003.gif\"/>都是会员玩家,何必太过嚣张</p>', '38', '14', '2019-02-13 10:05:10');
INSERT INTO `comment` VALUES ('39', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0009.gif\"/><span style=\"color: rgb(51, 51, 51); font-family: &quot;Microsoft YaHei&quot;, sans-serif; font-size: 14px; background-color: rgb(255, 255, 255);\">都是会员玩家,何必太过嚣张!</span></p>', '38', '14', '2019-02-13 10:06:19');
INSERT INTO `comment` VALUES ('40', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0004.gif\"/></p>', '38', '14', '2019-02-13 10:25:05');
INSERT INTO `comment` VALUES ('41', '<p><img src=\"http://img.baidu.com/hi/jx2/j_0022.gif\"/></p>', '38', '15', '2019-02-13 11:26:12');

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(5) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  KEY `star` (`star`) USING BTREE,
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of movie
-- ----------------------------
INSERT INTO `movie` VALUES ('24', '萌萌哒', '20190126140836b0eb6cc76e97492c9a825124aa8f5443.mp4', '萌萌哒', '2019012614083619dff1c0f5244e57867ed49402a532b0.jpg', '3', '0', '0', '1', '中国', '2019-01-30', '3', '2019-01-26 14:08:37');
INSERT INTO `movie` VALUES ('25', '卡哇伊', '20190126140906da8d9fb9d13b42e78fff2c1762fb36ee.mp4', '萌萌哒萌萌哒萌萌哒萌萌哒萌萌哒', '201901261409069af6be68b1e248c6be24a6bc472ea7a8.jpg', '2', '1', '0', '4', '中国', '2019-01-24', '3', '2019-01-26 14:09:06');
INSERT INTO `movie` VALUES ('26', '小可爱', '201901261409418e1309f023ee421ea7496189a26850dd.mp4', '萌萌哒萌萌哒萌萌哒萌萌哒', '20190126140941ae60f7037ace4cf6b34c8cbddcd28126.jpg', '1', '0', '0', '1', '中国', '2019-01-26', '3', '2019-01-26 14:09:41');
INSERT INTO `movie` VALUES ('33', '岛国小电影', '20190128113651e934fedc650340ccb4887395da3d5746.mp4', '岛国小电影', '2019012811365122b6c991dda240569a7fa6cae60b1a5d.jpg', '5', '0', '0', '3', '美国', '2019-02-03', '4', '2019-01-28 11:36:51');
INSERT INTO `movie` VALUES ('36', '331231321321', '20190212232009ac7772053c8e460db66e182288e14d43.mp4', '321', '2019012811521884272a92d8c9460ba51384d218a7373c.jpg', '4', '2', '0', '13', '中国', '2019-01-24', '3', '2019-01-28 11:52:18');
INSERT INTO `movie` VALUES ('38', '流浪地球', '20190212200500ae24a4161cd448139521f26bce873a82.mp4', '321321', '20190214113402c42378426a384112b6c70054b473856f.jpg', '1', '51', '2', '11', '中国', '2019-01-24', '3', '2019-01-28 11:53:12');
INSERT INTO `movie` VALUES ('39', '毒液', '20190214112633c12e36965eec47c9b3696eb3c4adb674.mp4', '《毒液：致命守护者》是美国哥伦比亚电影公司、腾讯影业、漫威影业联合出品，索尼电影娱乐公司发行的科幻电影，由鲁本·弗雷斯彻执导，汤姆·哈迪、米歇尔·威廉姆斯、里兹·阿迈德等人主演。\r\n影片改编自漫威漫画，讲述了埃迪·布洛克受到不明外星物质共生体的入侵与控制，成为亦正亦邪的另类超级英雄的故事', '201902141126336f1f6557211d4b66a1bbf1275deaff0f.jpg', '5', '2', '0', '1', '美国', '2019-01-24', '2', '2019-02-14 11:26:34');

-- ----------------------------
-- Table structure for moviecol
-- ----------------------------
DROP TABLE IF EXISTS `moviecol`;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of moviecol
-- ----------------------------
INSERT INTO `moviecol` VALUES ('36', '38', '7', '2019-01-28 15:00:46');
INSERT INTO `moviecol` VALUES ('37', '38', '14', '2019-02-13 10:46:56');
INSERT INTO `moviecol` VALUES ('38', '36', '14', '2019-02-13 11:04:27');

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of oplog
-- ----------------------------
INSERT INTO `oplog` VALUES ('1', '1', '127.0.0.1', '添加标签恐怖', '2019-01-28 10:58:14');
INSERT INTO `oplog` VALUES ('2', '1', '127.0.0.1', '添加标签色情', '2019-01-28 10:58:17');
INSERT INTO `oplog` VALUES ('3', '1', '127.0.0.1', '修改标签经典', '2019-01-28 11:27:53');
INSERT INTO `oplog` VALUES ('4', '1', '127.0.0.1', '标签搞笑修改为温暖', '2019-01-28 11:30:02');
INSERT INTO `oplog` VALUES ('5', '1', '127.0.0.1', '标签\" 温暖 \"修改为\" 亲情 \"', '2019-01-28 11:30:46');
INSERT INTO `oplog` VALUES ('6', '1', '127.0.0.1', '添加标签abc', '2019-01-28 11:32:30');
INSERT INTO `oplog` VALUES ('7', '1', '127.0.0.1', '删除 abc 标签', '2019-01-28 11:32:33');
INSERT INTO `oplog` VALUES ('8', '1', '127.0.0.1', '添加 岛国小电影 电影', '2019-01-28 11:36:51');
INSERT INTO `oplog` VALUES ('9', '1', '127.0.0.1', '添加 331231321321 电影', '2019-01-28 11:52:18');
INSERT INTO `oplog` VALUES ('10', '1', '127.0.0.1', '添加 3312313213211 电影', '2019-01-28 11:52:47');
INSERT INTO `oplog` VALUES ('11', '1', '127.0.0.1', '添加 我爱国 电影', '2019-01-28 11:53:12');
INSERT INTO `oplog` VALUES ('12', '1', '127.0.0.1', 'imoocmovie修改密码', '2019-01-28 13:26:55');
INSERT INTO `oplog` VALUES ('13', '1', '127.0.0.1', '删除 3312313213211 电影', '2019-01-28 13:29:21');
INSERT INTO `oplog` VALUES ('14', '1', '127.0.0.1', '修改 我爱国 电影', '2019-01-28 13:50:59');
INSERT INTO `oplog` VALUES ('15', '1', '127.0.0.1', '添加 小姐姐1232 上映预告', '2019-01-28 13:52:38');
INSERT INTO `oplog` VALUES ('16', '1', '127.0.0.1', '添加 小姐姐1232 上映预告', '2019-01-28 13:53:18');
INSERT INTO `oplog` VALUES ('17', '1', '127.0.0.1', '修改 木乃伊12 上映预告', '2019-01-28 13:54:25');
INSERT INTO `oplog` VALUES ('18', '1', '127.0.0.1', '删除 蛇 会员', '2019-01-28 13:57:25');
INSERT INTO `oplog` VALUES ('19', '1', '127.0.0.1', '删除 1 会员用户', '2019-01-28 14:08:50');
INSERT INTO `oplog` VALUES ('20', '1', '127.0.0.1', '删除 1 会员用户', '2019-01-28 14:12:56');
INSERT INTO `oplog` VALUES ('21', '1', '127.0.0.1', '删除 马 用户评论 内容: 不好看 ', '2019-01-28 14:38:19');
INSERT INTO `oplog` VALUES ('22', '1', '127.0.0.1', '删除 <羊> 用户评论的内容:< 还行 >', '2019-01-28 14:39:01');
INSERT INTO `oplog` VALUES ('23', '1', '127.0.0.1', '删除 <鼠> 用户所收藏的电影', '2019-01-28 15:01:37');
INSERT INTO `oplog` VALUES ('24', '1', '127.0.0.1', '删除 <兔> 用户所收藏的电影', '2019-01-28 15:02:19');
INSERT INTO `oplog` VALUES ('25', '1', '127.0.0.1', '删除 <牛> 用户所收藏的电影', '2019-01-28 15:02:36');
INSERT INTO `oplog` VALUES ('26', '1', '127.0.0.1', '删除 <虎> 用户收藏的电影 <小可爱>', '2019-01-28 15:03:37');
INSERT INTO `oplog` VALUES ('27', '1', '127.0.0.1', '添加 温暖 标签', '2019-01-28 16:09:51');
INSERT INTO `oplog` VALUES ('28', '1', '127.0.0.1', '删除 abc 权限', '2019-01-28 16:12:21');
INSERT INTO `oplog` VALUES ('29', '1', '127.0.0.1', '修改\" 用户登陆日志列表查询1 \"权限', '2019-01-28 16:20:11');
INSERT INTO `oplog` VALUES ('30', '1', '127.0.0.1', '修改\" 用户登陆日志列表查询 \"权限', '2019-01-28 16:20:15');
INSERT INTO `oplog` VALUES ('31', '1', '127.0.0.1', '删除 标签管理员 权限', '2019-01-28 17:22:53');
INSERT INTO `oplog` VALUES ('32', '1', '127.0.0.1', '修改\" 用户登陆日志列表查询1 \"权限', '2019-01-28 17:23:53');
INSERT INTO `oplog` VALUES ('33', '1', '127.0.0.1', '删除 用户登陆日志列表查询1 权限', '2019-01-28 17:23:53');
INSERT INTO `oplog` VALUES ('34', '1', '127.0.0.1', '修改\" 用户登陆日志列表查询 \"权限', '2019-01-28 17:24:17');
INSERT INTO `oplog` VALUES ('35', '1', '127.0.0.1', '删除 用户登陆日志列表查询 权限', '2019-01-28 17:24:17');
INSERT INTO `oplog` VALUES ('36', '1', '127.0.0.1', '添加 12 权限', '2019-01-28 17:26:09');
INSERT INTO `oplog` VALUES ('37', '1', '127.0.0.1', '删除 12 权限', '2019-01-28 17:26:20');
INSERT INTO `oplog` VALUES ('38', '1', '127.0.0.1', '添加 321 权限', '2019-01-28 17:27:27');
INSERT INTO `oplog` VALUES ('39', '1', '127.0.0.1', '删除 321 权限', '2019-01-28 17:27:34');
INSERT INTO `oplog` VALUES ('40', '1', '127.0.0.1', '添加 321 权限', '2019-01-28 17:27:56');
INSERT INTO `oplog` VALUES ('41', '1', '127.0.0.1', '删除 321 权限', '2019-01-28 17:28:03');
INSERT INTO `oplog` VALUES ('42', '1', '127.0.0.1', '删除 标签管理 权限', '2019-01-31 17:50:48');
INSERT INTO `oplog` VALUES ('43', '1', '127.0.0.1', '删除 超级管理员 权限', '2019-01-31 17:51:29');
INSERT INTO `oplog` VALUES ('44', '1', '127.0.0.1', '删除 标签管理员 权限', '2019-01-31 17:52:15');
INSERT INTO `oplog` VALUES ('45', '1', '127.0.0.1', '删除 标签管理员 权限', '2019-01-31 18:16:12');
INSERT INTO `oplog` VALUES ('46', '1', '127.0.0.1', '删除 测试添加 权限', '2019-01-31 18:21:30');
INSERT INTO `oplog` VALUES ('47', '1', '127.0.0.1', '修改\" 测试 \"权限', '2019-01-31 18:24:37');
INSERT INTO `oplog` VALUES ('48', '1', '127.0.0.1', '添加 abc123 管理员', '2019-02-01 09:26:20');
INSERT INTO `oplog` VALUES ('49', '1', '127.0.0.1', '添加 def123 管理员', '2019-02-01 09:27:35');
INSERT INTO `oplog` VALUES ('50', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 09:50:06');
INSERT INTO `oplog` VALUES ('51', '1', '127.0.0.1', '添加 超级管理员 管理员', '2019-02-01 09:51:59');
INSERT INTO `oplog` VALUES ('52', '1', '127.0.0.1', '添加 abc 标签', '2019-02-01 10:22:11');
INSERT INTO `oplog` VALUES ('53', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 10:25:36');
INSERT INTO `oplog` VALUES ('54', '1', '127.0.0.1', '删除 abc 标签', '2019-02-01 10:31:08');
INSERT INTO `oplog` VALUES ('55', '1', '127.0.0.1', '添加 查看会员 权限', '2019-02-01 10:38:54');
INSERT INTO `oplog` VALUES ('56', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 10:39:43');
INSERT INTO `oplog` VALUES ('57', '1', '127.0.0.1', '修改\" 编辑标签 \"权限', '2019-02-01 10:40:49');
INSERT INTO `oplog` VALUES ('58', '1', '127.0.0.1', '修改\" 编辑标签 \"权限', '2019-02-01 10:43:04');
INSERT INTO `oplog` VALUES ('59', '1', '127.0.0.1', '修改\" 编辑标签 \"权限', '2019-02-01 10:43:08');
INSERT INTO `oplog` VALUES ('60', '1', '127.0.0.1', '修改\" 会员列表 \"权限', '2019-02-01 12:07:32');
INSERT INTO `oplog` VALUES ('61', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 12:07:41');
INSERT INTO `oplog` VALUES ('62', '1', '127.0.0.1', '修改\" 查看会员 \"权限', '2019-02-01 12:09:00');
INSERT INTO `oplog` VALUES ('63', '1', '127.0.0.1', '删除 <兔> 用户评论的内容:< 给力 >', '2019-02-01 12:09:10');
INSERT INTO `oplog` VALUES ('64', '1', '127.0.0.1', '添加 收藏列表 权限', '2019-02-01 12:10:47');
INSERT INTO `oplog` VALUES ('65', '1', '127.0.0.1', '删除 <龙> 用户收藏的电影 <331231321321>', '2019-02-01 12:14:00');
INSERT INTO `oplog` VALUES ('66', '1', '127.0.0.1', '添加 添加管理员 权限', '2019-02-01 12:15:23');
INSERT INTO `oplog` VALUES ('67', '1', '127.0.0.1', '添加 管理员列表 权限', '2019-02-01 12:15:45');
INSERT INTO `oplog` VALUES ('68', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 12:16:00');
INSERT INTO `oplog` VALUES ('69', '1', '127.0.0.1', '添加 添加权限 权限', '2019-02-01 12:18:39');
INSERT INTO `oplog` VALUES ('70', '1', '127.0.0.1', '添加 权限列表 权限', '2019-02-01 12:18:58');
INSERT INTO `oplog` VALUES ('71', '1', '127.0.0.1', '添加 删除权限 权限', '2019-02-01 12:19:10');
INSERT INTO `oplog` VALUES ('72', '1', '127.0.0.1', '添加 编辑权限 权限', '2019-02-01 12:19:21');
INSERT INTO `oplog` VALUES ('73', '1', '127.0.0.1', '修改\" 超级管理员 \"权限', '2019-02-01 12:20:09');
INSERT INTO `oplog` VALUES ('74', '1', '127.0.0.1', '添加 知否知否应是绿肥红瘦 上映预告', '2019-02-12 16:34:04');
INSERT INTO `oplog` VALUES ('75', '1', '127.0.0.1', '添加 周杰伦 上映预告', '2019-02-12 16:37:24');
INSERT INTO `oplog` VALUES ('76', '1', '127.0.0.1', '添加 木乃伊 上映预告', '2019-02-12 16:49:18');
INSERT INTO `oplog` VALUES ('77', '1', '127.0.0.1', '添加 校花 上映预告', '2019-02-12 16:49:40');
INSERT INTO `oplog` VALUES ('78', '1', '127.0.0.1', '添加 小姐姐321 上映预告', '2019-02-12 16:49:50');
INSERT INTO `oplog` VALUES ('79', '1', '127.0.0.1', '添加 木乃伊1 上映预告', '2019-02-12 16:49:55');
INSERT INTO `oplog` VALUES ('80', '1', '127.0.0.1', '添加 校花32131 上映预告', '2019-02-12 16:50:18');
INSERT INTO `oplog` VALUES ('81', '1', '127.0.0.1', '添加 神剧 上映预告', '2019-02-12 16:51:01');
INSERT INTO `oplog` VALUES ('82', '1', '127.0.0.1', '添加 掏粪男孩 上映预告', '2019-02-12 16:51:10');
INSERT INTO `oplog` VALUES ('83', '1', '127.0.0.1', '添加 王力宏 上映预告', '2019-02-12 16:51:18');
INSERT INTO `oplog` VALUES ('84', '1', '127.0.0.1', '添加 呜呜呜 上映预告', '2019-02-12 16:51:26');
INSERT INTO `oplog` VALUES ('85', '1', '127.0.0.1', '添加 武则天 上映预告', '2019-02-12 16:51:35');
INSERT INTO `oplog` VALUES ('86', '1', '127.0.0.1', '添加 知否知否应是绿肥红瘦 上映预告', '2019-02-12 18:15:29');
INSERT INTO `oplog` VALUES ('87', '1', '127.0.0.1', '添加 垃圾 上映预告', '2019-02-12 18:21:31');
INSERT INTO `oplog` VALUES ('88', '1', '127.0.0.1', '修改 我爱国 电影', '2019-02-12 20:05:01');
INSERT INTO `oplog` VALUES ('89', '1', '127.0.0.1', '修改 我爱国 电影', '2019-02-12 20:13:16');
INSERT INTO `oplog` VALUES ('90', '1', '127.0.0.1', '修改 我爱国 电影', '2019-02-12 20:13:32');
INSERT INTO `oplog` VALUES ('91', '1', '127.0.0.1', '修改 331231321321 电影', '2019-02-12 23:20:09');
INSERT INTO `oplog` VALUES ('92', '1', '127.0.0.1', '修改 331231321321 电影', '2019-02-12 23:21:28');
INSERT INTO `oplog` VALUES ('93', '1', '127.0.0.1', '添加 毒液 电影', '2019-02-14 11:26:34');
INSERT INTO `oplog` VALUES ('94', '1', '127.0.0.1', '修改 呜呜呜 上映预告', '2019-02-14 11:30:06');
INSERT INTO `oplog` VALUES ('95', '1', '127.0.0.1', '修改 毒液 上映预告', '2019-02-14 11:30:17');
INSERT INTO `oplog` VALUES ('96', '1', '127.0.0.1', '修改 来电狂响 上映预告', '2019-02-14 11:31:41');
INSERT INTO `oplog` VALUES ('97', '1', '127.0.0.1', '删除 掏粪男孩 上映预告', '2019-02-14 11:32:05');
INSERT INTO `oplog` VALUES ('98', '1', '127.0.0.1', '修改 流浪地球 上映预告', '2019-02-14 11:33:24');
INSERT INTO `oplog` VALUES ('99', '1', '127.0.0.1', '修改 流浪地球 电影', '2019-02-14 11:34:03');

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of preview
-- ----------------------------
INSERT INTO `preview` VALUES ('4', '来电狂响', '20190214113141208ef496e7fa4b558ba3a3917b4b4710.jpg', '2019-02-12 16:37:24');
INSERT INTO `preview` VALUES ('12', '流浪地球', '20190214113323a3bb703ffc9643a8974da8863f07bf4d.jpg', '2019-02-12 16:51:18');
INSERT INTO `preview` VALUES ('13', '毒液', '20190214113017bd9a442bf7314926842685fe20ffe2e0.jpg', '2019-02-12 16:51:26');
INSERT INTO `preview` VALUES ('15', '知否知否应是绿肥红瘦', '201902121815299bef4acd64794438a414de91383b73c8.jpg', '2019-02-12 18:15:29');
INSERT INTO `preview` VALUES ('16', '垃圾', '20190212182131b05d142c9c4446d789d72624eca85e0e.jpg', '2019-02-12 18:21:31');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('8', '标签管理员', '3,7', '2019-01-31 18:16:19');
INSERT INTO `role` VALUES ('10', '测试', '3,4,5,7', '2019-01-31 18:21:38');
INSERT INTO `role` VALUES ('11', '超级管理员', '3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,27,28,29,30,31,32,33', '2019-02-01 09:48:14');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES ('1', '动作', '2019-01-25 13:18:32');
INSERT INTO `tag` VALUES ('2', '爱情', '2019-01-25 13:18:52');
INSERT INTO `tag` VALUES ('3', '亲情', '2019-01-25 14:12:56');
INSERT INTO `tag` VALUES ('4', '怀旧', '2019-01-25 14:13:14');
INSERT INTO `tag` VALUES ('8', '科幻', '2019-01-25 15:02:05');
INSERT INTO `tag` VALUES ('11', '经典', '2019-01-28 10:58:17');
INSERT INTO `tag` VALUES ('13', '温暖', '2019-01-28 16:09:51');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '鼠', '1231', '1231@123.com', '13888888881', '鼠', '1f401.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc0');
INSERT INTO `user` VALUES ('2', '牛', '1232', '1232@123.com', '13888888882', '牛', '1f402.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc1');
INSERT INTO `user` VALUES ('3', '虎', '1233', '1233@123.com', '13888888883', '虎', '1f405.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc2');
INSERT INTO `user` VALUES ('4', '兔', '1234', '1234@123.com', '13888888884', '兔', '1f407.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc3');
INSERT INTO `user` VALUES ('5', '龙', '1235', '1235@123.com', '13888888885', '龙', '1f409.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc4');
INSERT INTO `user` VALUES ('7', '马', '1237', '1237@123.com', '13888888887', '马', '1f434.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc6');
INSERT INTO `user` VALUES ('8', '羊', '1238', '1238@123.com', '13888888888', '羊', '1f411.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc7');
INSERT INTO `user` VALUES ('9', '猴', '1239', '1239@123.com', '13888888889', '猴', '1f412.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc8');
INSERT INTO `user` VALUES ('10', '鸡', '1240', '1240@123.com', '13888888891', '鸡', '1f413.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fc9');
INSERT INTO `user` VALUES ('11', '狗', '1241', '1241@123.com', '13888888892', '狗', '1f415.png', '2019-01-26 13:30:17', 'd32a72bdac524478b7e4f6dfc8394fd0');
INSERT INTO `user` VALUES ('12', '你大爷', 'pbkdf2:sha256:50000$H7fxxGD0$1b1887b5430149b45313cf6be8df27fb3cdd8954a835189c7ea135b9ae04f4be', '2442009349@qq.com', '18022445503', '321321', '2019021310021454431f42f5134e88a60327639f7c5357.jpg', '2019-02-12 09:36:03', 'dd332534b81b4b8db5b872eb80694883');
INSERT INTO `user` VALUES ('13', 'adimin', 'pbkdf2:sha256:50000$sUCMZGBV$83a17d47d4e35994401809889b20826dc70f6b7ad0fffd747d0825eb3772a932', '2442009359@qq.com', '18022445504', null, null, '2019-02-12 19:13:46', 'fde66283e2da4732bc5e984cb51095d6');
INSERT INTO `user` VALUES ('14', '你二大爷', 'pbkdf2:sha256:50000$CnxWNGfL$943a1c6ba66399b4887564e599550ca06338e053085cdeb1386324b0cdb60d50', '2442009309@qq.com', '18022445505', '123', '2019021310060294ecc49da49242a29dfc998826e8fb00.jpg', '2019-02-13 10:04:31', '0c0846a3724f4164b693d6773f8a9c76');
INSERT INTO `user` VALUES ('15', '你三大爷', 'pbkdf2:sha256:50000$YvTkRPuP$ce716b41170c31174c0d5a829e23949fc7b1c1213cd1462ef3fd42ea9ea691ba', '244@qq.com', '18022445506', null, null, '2019-02-13 11:25:57', '5639bbf2821c40e0859286a512a3109e');

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userlog
-- ----------------------------
INSERT INTO `userlog` VALUES ('1', '1', '192.168.4.1', '2019-01-28 11:18:22');
INSERT INTO `userlog` VALUES ('2', '2', '192.168.4.2', '2019-01-28 11:18:22');
INSERT INTO `userlog` VALUES ('18', '12', '127.0.0.1', '2019-02-12 13:13:13');
INSERT INTO `userlog` VALUES ('19', '12', '127.0.0.1', '2019-02-12 14:26:47');
INSERT INTO `userlog` VALUES ('20', '12', '127.0.0.1', '2019-02-12 15:32:21');
INSERT INTO `userlog` VALUES ('21', '12', '127.0.0.1', '2019-02-12 15:50:13');
INSERT INTO `userlog` VALUES ('22', '12', '127.0.0.1', '2019-02-12 15:50:28');
INSERT INTO `userlog` VALUES ('23', '12', '127.0.0.1', '2019-02-12 15:50:48');
INSERT INTO `userlog` VALUES ('24', '12', '127.0.0.1', '2019-02-12 15:50:52');
INSERT INTO `userlog` VALUES ('25', '12', '127.0.0.1', '2019-02-12 15:50:56');
INSERT INTO `userlog` VALUES ('26', '12', '127.0.0.1', '2019-02-12 15:51:07');
INSERT INTO `userlog` VALUES ('27', '12', '127.0.0.1', '2019-02-12 15:51:36');
INSERT INTO `userlog` VALUES ('28', '12', '127.0.0.1', '2019-02-12 15:51:40');
INSERT INTO `userlog` VALUES ('29', '12', '127.0.0.1', '2019-02-12 15:51:44');
INSERT INTO `userlog` VALUES ('30', '12', '127.0.0.1', '2019-02-12 15:51:48');
INSERT INTO `userlog` VALUES ('31', '12', '127.0.0.1', '2019-02-12 19:20:30');
INSERT INTO `userlog` VALUES ('32', '12', '127.0.0.1', '2019-02-12 19:55:40');
INSERT INTO `userlog` VALUES ('33', '12', '127.0.0.1', '2019-02-13 09:13:35');
INSERT INTO `userlog` VALUES ('34', '12', '127.0.0.1', '2019-02-13 09:14:06');
INSERT INTO `userlog` VALUES ('35', '12', '127.0.0.1', '2019-02-13 09:16:00');
INSERT INTO `userlog` VALUES ('36', '14', '127.0.0.1', '2019-02-13 10:04:39');
INSERT INTO `userlog` VALUES ('37', '15', '127.0.0.1', '2019-02-13 11:26:02');
