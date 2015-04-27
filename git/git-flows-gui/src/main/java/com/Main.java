package com;

import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.html.HTMLFormElement;
import org.w3c.dom.html.HTMLInputElement;
import javafx.stage.DirectoryChooser;

import java.io.File;

public class Main extends Application {

    @Override
    public void start(Stage st) throws Exception {
        VBox root = new VBox();
        Button bt = new Button("Actuar");
        Button bt2 = new Button("Select");

        WebView w = new WebView();

        WebEngine engine = w.getEngine();

        engine.load("file:///D:/MisDocumentos/src/git-utilities/git/git-flows-gui/index.html");

        bt.setOnAction(event -> {
            String jqueryScript = "http://localhost:8000/static/cdn/jquery-2.1.3.js";
//            String lodashScript = "http://localhost:8000/static/cdn/lodash-3.7.0.js";
            engine.executeScript("(function() { "
                            + "  var script = document.createElement(\"script\");"
                            + "  script.type = \"text/javascript\";"
                            + "  script.src = \"" + jqueryScript + "\";"
                            + "  script.onload = script.onreadystatechange = function() {"
                            + "    $(\"#llave\").html(232323);"
                            + "  };"
                            + "  document.documentElement.childNodes[0].appendChild(script);"
                            + "})();"
            );
        });

        bt2.setOnAction(event -> {

            DirectoryChooser dch = new DirectoryChooser();

            dch.setTitle("Seleccione repositorio");

            File file = dch.showDialog(st.getOwner());
            if (file != null) {
                System.out.println("Escogido: " + file.getAbsolutePath());
            } else {
                System.out.println("no");
            }

        });


        root.getChildren().addAll(bt, bt2, w);
        st.setScene(new Scene(root, 600, 600));
        st.show();
    }

    public static void main(String[] args) {
        launch(args);
    }

}
