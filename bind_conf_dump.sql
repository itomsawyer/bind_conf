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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  `grp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ipnet_UNIQUE` (`ipnet`),
  KEY `grp_id_idx` (`grp_id`),
  CONSTRAINT `fk_ipnet_grp_id` FOREIGN KEY (`grp_id`) REFERENCES `dns_forward_ipnet_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_ipnet`
--

LOCK TABLES `dns_forward_ipnet` WRITE;
/*!40000 ALTER TABLE `dns_forward_ipnet` DISABLE KEYS */;
INSERT INTO `dns_forward_ipnet` VALUES (1,'any',0,1);
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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_ipnet_grp`
--

LOCK TABLES `dns_forward_ipnet_grp` WRITE;
/*!40000 ALTER TABLE `dns_forward_ipnet_grp` DISABLE KEYS */;
INSERT INTO `dns_forward_ipnet_grp` VALUES (1,'default',99,0);
/*!40000 ALTER TABLE `dns_forward_ipnet_grp` ENABLE KEYS */;
UNLOCK TABLES;

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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `grp_id_idx` (`grp_id`),
  CONSTRAINT `fk_zone_grp_id` FOREIGN KEY (`grp_id`) REFERENCES `dns_forward_zone_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_zone`
--

LOCK TABLES `dns_forward_zone` WRITE;
/*!40000 ALTER TABLE `dns_forward_zone` DISABLE KEYS */;
INSERT INTO `dns_forward_zone` VALUES (1,'.','only',1,0);
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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dm_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forward_zone_grp`
--

LOCK TABLES `dns_forward_zone_grp` WRITE;
/*!40000 ALTER TABLE `dns_forward_zone_grp` DISABLE KEYS */;
INSERT INTO `dns_forward_zone_grp` VALUES (1,'default',0);
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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `zone_id_idx` (`zone_grp_id`),
  KEY `ldns_id_idx` (`ldns_id`),
  KEY `ipnet_grp_id_idx` (`ipnet_grp_id`),
  CONSTRAINT `fk_fw_ipnet_grp_id` FOREIGN KEY (`ipnet_grp_id`) REFERENCES `dns_forward_ipnet_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_fw_ldns_id` FOREIGN KEY (`ldns_id`) REFERENCES `ldns` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_fw_zone_grp_id` FOREIGN KEY (`zone_grp_id`) REFERENCES `dns_forward_zone_grp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dns_forwarders`
--

LOCK TABLES `dns_forwarders` WRITE;
/*!40000 ALTER TABLE `dns_forwarders` DISABLE KEYS */;
INSERT INTO `dns_forwarders` VALUES (1,1,1,1,0);
/*!40000 ALTER TABLE `dns_forwarders` ENABLE KEYS */;
UNLOCK TABLES;

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
  `disabled` tinyint(4) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  UNIQUE KEY `addr_UNIQUE` (`addr`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ldns`
--

LOCK TABLES `ldns` WRITE;
/*!40000 ALTER TABLE `ldns` DISABLE KEYS */;
INSERT INTO `ldns` VALUES (1,'default','223.5.5.5',0,0),(2,'ali_public_dns','223.6.6.6',0,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Admin',NULL,'admin','admin',1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-21 15:09:30
