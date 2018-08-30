#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import demjson
import pymysql
import codecs
import chardet
import traceback
#连接数据库
conn = pymysql.connect(host="192.168.15.213",user="root",passwd="root",db="vrdata") #centos6虚拟机
#conn = pymysql.connect("47.105.122.253", "mhtvr168", "123456", "mhtvr168")  #华北
#conn = pymysql.connect("120.77.172.47", "root", "root", "mhtvr168")   #华南
cur = conn.cursor()#创建游标

#打开输出文件
file_sql = codecs.open("import.sql", "w", "utf-8")

try:
    #打开配置文件1
    with open("htpfilm.hts", "rb") as file_json:
        content = file_json.read()

        #解析配置文件的json数据
        film_list = demjson.decode(content)

        deleteSql = 'DELETE FROM htproductfilm;'
        reCount = cur.execute(deleteSql)
        file_sql.write('%s\n' % deleteSql)

        for i, val in enumerate(film_list):  #遍历list
            file_sql.write(val)
            file_sql.write("\n")
            #print("操作数据库(序号:%s), sql : %s" % (i+1, val))
            reCount = cur.execute(val)
        print("操作htpfilm.hts成功")
except FileNotFoundError:
    print("文件htpfilm.hts不存在，不处理")
except:
    print("操作htpfilm.hts失败，失败原因:\n")
    traceback.print_exc()

try:
    #打开输出文件2
    with open("VRFilm0.hts", "rb") as file_json2:
        content2 = file_json2.read()
        product_list2 = demjson.decode(content2)

        deleteSql2 = 'DELETE FROM filmlist;'
        reCount = cur.execute(deleteSql2)
        file_sql.write('%s\n' % deleteSql2)

        for i, val in enumerate(product_list2):
            sql = ""
            if 'GlassesType' in val:
                sql = u'insert into filmlist(FilmID, FilmName, FilmNameEn, ShowOrder, FilmType, FilmClassID, FilmShow, FilmLong, FilmTypeID, GlassesType, AuthorityLv) values(%s,"%s","%s",%s,%s,%s,%s,%s,%s,%s,%s);'%(val["FilmID"],val["FilmName"],val["FilmNameEn"],val["ShowOrder"],val["FilmType"],val["FilmClassID"],"1","0",val["FilmTypeID"],val["GlassesType"],"1")
            else:
                sql = u'insert into filmlist(FilmID, FilmName, FilmNameEn, ShowOrder, FilmType, FilmClassID, FilmShow, FilmLong, FilmTypeID, GlassesType, AuthorityLv) values(%s,"%s","%s",%s,%s,%s,%s,%s,%s,%s,%s);'%(val["FilmID"],val["FilmName"],val["FilmNameEn"],val["ShowOrder"],val["FilmType"],val["FilmClassID"],"1","0",val["FilmTypeID"],"1073741823","1")
                #print ("操作数据库(序号:%s), sql : %s" % (i, sql))
                file_sql.write(sql)
                file_sql.write("\n")
                reCount = cur.execute(sql)
        print("操作VRFilm0.hts成功")
except FileNotFoundError:
    print("文件VRFilm0.hts不存在，不处理")
except Exception as e:
    print("操作VRFilm0.hts失败，失败原因: \n")
    traceback.print_exc()
    #print('%s' % traceback.format_exc())

file_sql.close()

conn.commit()#提交数据到数据库
cur.close()
conn.close()

