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

import config.GAConfig

import scala.collection.immutable.Range
import scala.sys.process._

object Main extends App {

  val conf = GAConfig.loadFromJSON("baseConfig.json")

  for (
    ce <- Range(1, 31);
    cr <- Range(1, 11) if (ce >= cr)
  ) {

    println("Calculating with < " + ce + " > evaluators, and < " + cr + " > reproducers")

    conf.setEvaluatorsCount(ce)
    conf.setReproducersCount(cr)

    conf.setSeqOutputFilename("./results/seqResults" + conf.toSufixName() + ".csv")
    conf.setParallelOutputFilename("./results/parResults" + conf.toSufixName() + ".csv")

    println("Scala is calculating...")
    execScalaApps()

    println("Clojure is calculating...")
    execClojureApps()

    println("Erlang is calculating...\n\n")
    execErlangApps()

  }

  //  "shutdown.bat"!!

  def execAndWait(cmd: String) = {
    var pb: Process = null

    pb = Process(cmd) run ProcessLogger(
      n => {
        println(n)
      },
      e => {
        println("Error>> " + e)
        //        pb.destroy
      })

    val res = pb.exitValue()
    println("exitValue: " + res)
    res
  }

  def execScalaApps() {
    GAConfig.saveToJSON(conf, "./scl/maxSATConfig.json")
    //    "scalaSeq.bat"!!
    execAndWait("scalaPar.bat")
  }

  def execClojureApps() {
    GAConfig.saveToJSON(conf, "./clj/maxSATConfig.json")
    //    "clojureSeq.bat"!!
    execAndWait("clojurePar.bat")
  }

  def execErlangApps() {
    GAConfig.saveToErlangModule(conf, "./erl/")
    //    "erlangSeq.bat"!!
    execAndWait("compileErlangConfig.bat")
    execAndWait("erlangPar.bat")
  }

}