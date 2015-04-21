/*
* Copyright (c) 2013, José Albert Cruz Almaguer <jalbertcruz@gmail.com>
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*
* 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

package main

import java.io.File

import com.github.tototoshi.csv._

import scala.collection.mutable.ArrayBuffer

object ResultsAnalysis extends App {

  def genSummary() {
    //    val langs = List("go")
    //    val langs = List("clj", "go", "j", "scl")
    val langs = List("clj", "erl", "scl")
    //    val langs = List("clj")

    langs.foreach(l => {
      mkSummarize("./data/", l, "seq", 0.05)
      mkSummarize("./data/", l, "par", 0.05)
    })

  }

  //  genSummary()

  //    println(genLineGraph4Reproducer("clj", 2))

  def genLineGraph4Reproducer(lang: String, repCount: Int): String = {
    val rdr = CSVReader.open(lang + "_par_results.csv")
    //    var header = rdr.readNext match { case Some(h) => h }
    val all = rdr.all.tail.toList
    rdr.close
    val evaluators4RepFixed =
      (for (l <- all if l(6).toDouble.toInt == repCount)
      yield (l(5), l(2))).map(par => (par._1.toDouble.toInt, par._2.toDouble)).
        sortWith((a: (Int, Double), b: (Int, Double)) => a._1 < b._1)
    val res = evaluators4RepFixed.mkString("\n\t")
    return res
  }

  def mkSummarize(home: String, lang: String, prefix: String, delta: Double) {
    val dir = new File(home + lang + "/results/")
    var head = List[String]()

    val summaries = new ArrayBuffer[(List[Double], Double, Int)]()
    var sel = false
    for (
      f <- dir.listFiles() if f.isFile &&
      f.getName.endsWith(".csv") &&
      f.getName.startsWith(prefix)
    ) {
      summaries += summarize(f, 0, delta)
      if (!sel) {
        head = getHeader(f)
        sel = true
      }
    }

    head = "standardDeviation" :: "noOfPeaks" :: head

    val wFile = new File(home + lang + "_" + prefix + "_results.csv")
    val writer = CSVWriter.open(wFile)

    writer.writeRow(head)
    writer.writeAll(summaries.map(e => e._2 :: e._3 :: e._1))

    writer.close
  }

  def getHeader(file: File) = {
    val rdr = CSVReader.open(file)
    rdr.readNext match {
      case Some(h) => h
      case _ => List[String]()
    }
  }

  def summarize(file: File, pos: Int, delta: Double) = {
    val rdr = CSVReader.open(file)
    //    var header = rdr.readNext match { case Some(h) => h }
    val all = rdr.all
    val header = all.head
    rdr.close

    val rows: ArrayBuffer[List[Double]] = new ArrayBuffer[List[Double]]()

    val rtmp = all.tail.map(_.map(_.toDouble))

    rtmp.foreach(rows += _)
    val initRowsLength = rows.length

    var sDev = 0.0
    var ave = 0.0
    var fin = false

    do {
      ave = average(rows, pos)
      sDev = standardDeviation(ave, rows, pos)

      if (sDev / ave > delta) {
        // Eliminar el valor mas lejano al ave
        val indices = 1 to rows.length - 1
        val pLejano = indices.foldLeft(0)((a: Int, b: Int) =>
          if (math.abs(math.abs(ave) - math.abs(rows(a)(pos))) < math.abs(math.abs(ave) - math.abs(rows(b)(pos))))
            b
          else a)
        rows.remove(pLejano)
      } else
        fin = true

    } while (!fin && !rows.isEmpty)

    val allAve = new Array[Double](header.length)

    for (
      c <- 0 to header.length - 1;
      r <- 0 to rows.length - 1
    ) allAve(c) += rows(r)(c)

    (allAve.map(_ / rows.length).toList, sDev, initRowsLength - rows.length)

  }

  def calcRowAve(file: File, row: Int): Double = {
    val rdr = CSVReader.open(file)
    val rtmp = rdr.all.tail.map(
      i => {
        i(row).toDouble
      }
    )

    rtmp.reduce((a, b) => a + b) / rtmp.length
  }

  def standardDeviation(ave: Double, rows: ArrayBuffer[List[Double]], pos: Int): Double = {
    val res = rows.foldLeft(0.0)((v: Double, a: List[Double]) => v + Math.pow(ave - a(pos), 2))
    Math.sqrt(res / rows.length)
  }

  def switchCSVColumms(file: File, ca: Int, cb: Int): Unit = {
    val rdr = CSVReader.open(file)
    val all = rdr.all
    val res = all.map(l => l.slice(0, ca) ++ List(l(cb)) ++ l.slice(ca + 1, cb) ++ List(l(ca)) ++ l.slice(cb + 1, l.length))
    val wFile = new File(file.getAbsolutePath + "_")
    val writer = CSVWriter.open(wFile)
    writer.writeAll(res)
    writer.close
  }

  def processToEvostar2015(home: String, lang: String, prefix: String): Unit = {
    val dir = new File(home + lang + "/results/")
    var head: List[String] = List()
    val summaries = new ArrayBuffer[(Int, Int, Iterable[Double])]()
    var sel = false
    for (
      f <- dir.listFiles() if f.isFile &&
      f.getName.endsWith(".csv") &&
      f.getName.startsWith(prefix)
    ) {
      if (!sel) {
        head = getHeader(f)
        sel = true
      }
      summarizeEvostar2015ResFile(f, -1, 424) match {
        case Some(x) => summaries += x
        case _ =>
      }
    }
    head = "TotalRuns" :: "EffectiveRuns" :: head
    val wFile = new File(home + lang + "_" + prefix + "_results.csv")
    val writer = CSVWriter.open(wFile)
    writer.writeRow(head)
    writer.writeAll(summaries.map(e => (e._1 :: e._2 :: e._3.toList)))
    writer.close

    //    val reproductores = List(1, 2)
    //    val evaluadores = List(2, 4, 8, 16, 32)
  }

  /** *
    *
    * @param file
    * @param posSol
    * @param solValue
    * @return (<Total runs>, <Effective runs>, <Averages>)
    */
  def summarizeEvostar2015ResFile(file: File, posSol: Int, solValue: Double): Option[(Int, Int, Iterable[Double])] = {
    val rdr = CSVReader.open(file)
    //    var header = rdr.readNext match { case Some(h) => h }
    val all = rdr.all
    val header = all.head
    rdr.close
    val pos = if (posSol < 0) posSol + header.length else posSol

    val rtmp = all.tail.map(_.map(_.toDouble))
    val rows = rtmp.filter(_(pos) >= solValue)
    if (rows.length > 0)
      Some((rtmp.length, rows.length, (0 to (header.length - 1)).map(average(rows, _))))
    else
      None
  }

  def average(rows: Iterable[List[Double]], pos: Int): Double = {
    val res = rows.foldLeft(0.0)((v: Double, a: List[Double]) => v + a(pos))
    res / rows.size
  }

  //  val f = new File("D:/Mis Documentos/PhD/src/sclEA/seqResults/seqResults.csv")
  //  val f1 = new File("D:/Mis Documentos/PhD/src/utilities/ResultsAnalysis/data/scl/results/seqResults.csv")
  //  val f2 = new File("D:/Mis Documentos/PhD/src/utilities/ResultsAnalysis/data/scl/results/seqResults.csv_")
  //
  //  switchCSVColumms(f1, 1, 2)
  //
  //  println(calcRowAve(f, 2))
  //  println(calcRowAve(f1, 2))
  //  println(calcRowAve(f2, 1))

  def genSummaryEvostar2015() {
    //    val langs = List("clj", "go", "j", "scl")
    //    val langs = List("clj", "erl", "scl")
    //    val langs = List("scl", "clj")
    //    val langs = List("go")
    val langs = List("clj", "go", "scl")

    langs.foreach(l => {
      processToEvostar2015("./data/", l, "seq")
      processToEvostar2015("./data/", l, "par")
    })

  }

  genSummaryEvostar2015()

}