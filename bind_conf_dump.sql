-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: bind_conf
-- ------------------------------------------------------
-- Server version	5.6.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dns_forward_ipnet`
--

DROP TABLE IF EXISTS `dns_forward_ipnet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dns_forward_ipnet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipnet` varchar(45) NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  `grp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ipnet_UNIQUE` (`ipnet`),
  KEY `grp_id_idx` (`grp_id`),
  CONSTRAINT `fk_ipnet_grp_id` FOREIGN KEY (`grp_id`) REFERENCES `dns_forward_ipnet_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_ipnet`
--

LOCK TABLES `dns_forward_ipnet` WRITE;
/*!40000 ALTER TABLE `dns_forward_ipnet` DISABLE KEYS */;
INSERT INTO `dns_forward_ipnet` VALUES (1,'any',1,1);
/*!40000 ALTER TABLE `dns_forward_ipnet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dns_forward_ipnet_grp`
--

DROP TABLE IF EXISTS `dns_forward_ipnet_grp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dns_forward_ipnet_grp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `prio` int(11) NOT NULL DEFAULT '10',
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_ipnet_grp`
--

LOCK TABLES `dns_forward_ipnet_grp` WRITE;
/*!40000 ALTER TABLE `dns_forward_ipnet_grp` DISABLE KEYS */;
INSERT INTO `dns_forward_ipnet_grp` VALUES (1,'default',99,1);
/*!40000 ALTER TABLE `dns_forward_ipnet_grp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `dns_forward_ipnet_view`
--

DROP TABLE IF EXISTS `dns_forward_ipnet_view`;
/*!50001 DROP VIEW IF EXISTS `dns_forward_ipnet_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `dns_forward_ipnet_view` AS SELECT 
 1 AS `name`,
 1 AS `prio`,
 1 AS `ipnet`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dns_forward_zone`
--

DROP TABLE IF EXISTS `dns_forward_zone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dns_forward_zone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `typ` varchar(45) NOT NULL DEFAULT 'only',
  `grp_id` int(11) NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `grp_id_idx` (`grp_id`),
  CONSTRAINT `fk_zone_grp_id` FOREIGN KEY (`grp_id`) REFERENCES `dns_forward_zone_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_zone`
--

LOCK TABLES `dns_forward_zone` WRITE;
/*!40000 ALTER TABLE `dns_forward_zone` DISABLE KEYS */;
INSERT INTO `dns_forward_zone` VALUES (1,'.','only',1,1);
/*!40000 ALTER TABLE `dns_forward_zone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dns_forward_zone_grp`
--

DROP TABLE IF EXISTS `dns_forward_zone_grp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dns_forward_zone_grp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dm_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_zone_grp`
--

LOCK TABLES `dns_forward_zone_grp` WRITE;
/*!40000 ALTER TABLE `dns_forward_zone_grp` DISABLE KEYS */;
INSERT INTO `dns_forward_zone_grp` VALUES (1,'default',1);
/*!40000 ALTER TABLE `dns_forward_zone_grp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dns_forwarders`
--

DROP TABLE IF EXISTS `dns_forwarders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dns_forwarders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `zone_grp_id` int(11) NOT NULL,
  `ipnet_grp_id` int(11) NOT NULL,
  `ldns_id` int(11) NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `zone_id_idx` (`zone_grp_id`),
  KEY `ldns_id_idx` (`ldns_id`),
  KEY `ipnet_grp_id_idx` (`ipnet_grp_id`),
  CONSTRAINT `fk_fw_ipnet_grp_id` FOREIGN KEY (`ipnet_grp_id`) REFERENCES `dns_forward_ipnet_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_fw_ldns_id` FOREIGN KEY (`ldns_id`) REFERENCES `ldns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_fw_zone_grp_id` FOREIGN KEY (`zone_grp_id`) REFERENCES `dns_forward_zone_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forwarders`
--

LOCK TABLES `dns_forwarders` WRITE;
/*!40000 ALTER TABLE `dns_forwarders` DISABLE KEYS */;
INSERT INTO `dns_forwarders` VALUES (1,1,1,1,1);
/*!40000 ALTER TABLE `dns_forwarders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `dns_forwarders_view`
--

DROP TABLE IF EXISTS `dns_forwarders_view`;
/*!50001 DROP VIEW IF EXISTS `dns_forwarders_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `dns_forwarders_view` AS SELECT 
 1 AS `view_name`,
 1 AS `view_prio`,
 1 AS `dm_zone`,
 1 AS `fwd_policy`,
 1 AS `ldns_name`,
 1 AS `ldns_addr`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ldns`
--

DROP TABLE IF EXISTS `ldns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ldns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `addr` varchar(45) NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `addr_UNIQUE` (`addr`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ldns`
--

LOCK TABLES `ldns` WRITE;
/*!40000 ALTER TABLE `ldns` DISABLE KEYS */;
INSERT INTO `ldns` VALUES (1,'default','223.5.5.5',1,1);
/*!40000 ALTER TABLE `ldns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'user',NULL),(2,'superuser',NULL);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles_users` (
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_users`
--

LOCK TABLES `roles_users` WRITE;
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO `roles_users` VALUES (1,1),(1,2);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Admin',NULL,'admin','$pbkdf2-sha512$25000$0zrnnPN.D4HQ.h/j3FuL0Q$xaPesYxR0W4dT4aPjTm0tExMNqtr3E1/a6H07kDDxgzVkw3mIanpVNlP52YDnyrf0lHAxesBPI0D.neRokix9g',1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `dns_forward_ipnet_view`
--

/*!50001 DROP VIEW IF EXISTS `dns_forward_ipnet_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `dns_forward_ipnet_view` AS select `dns_forward_ipnet_grp`.`name` AS `name`,`dns_forward_ipnet_grp`.`prio` AS `prio`,`dns_forward_ipnet`.`ipnet` AS `ipnet` from (`dns_forward_ipnet_grp` join `dns_forward_ipnet`) where ((`dns_forward_ipnet`.`grp_id` = `dns_forward_ipnet_grp`.`id`) and (`dns_forward_ipnet_grp`.`enabled` = 1) and (`dns_forward_ipnet`.`enabled` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `dns_forwarders_view`
--

/*!50001 DROP VIEW IF EXISTS `dns_forwarders_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `dns_forwarders_view` AS select `dns_forward_ipnet_grp`.`name` AS `view_name`,`dns_forward_ipnet_grp`.`prio` AS `view_prio`,`dns_forward_zone`.`name` AS `dm_zone`,`dns_forward_zone`.`typ` AS `fwd_policy`,`ldns`.`name` AS `ldns_name`,`ldns`.`addr` AS `ldns_addr` from ((((`dns_forwarders` join `dns_forward_zone_grp`) join `dns_forward_ipnet_grp`) join `ldns`) join `dns_forward_zone`) where ((`dns_forwarders`.`zone_grp_id` = `dns_forward_zone_grp`.`id`) and (`dns_forwarders`.`ipnet_grp_id` = `dns_forward_ipnet_grp`.`id`) and (`dns_forwarders`.`ldns_id` = `ldns`.`id`) and (`dns_forward_zone_grp`.`id` = `dns_forward_zone`.`grp_id`) and (`dns_forwarders`.`enabled` = 1) and (`dns_forward_zone_grp`.`enabled` = 1) and (`dns_forward_ipnet_grp`.`enabled` = 1) and (`ldns`.`status` = 1) and (`ldns`.`enabled` = 1) and (`dns_forward_zone`.`enabled` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-22 13:52:04
