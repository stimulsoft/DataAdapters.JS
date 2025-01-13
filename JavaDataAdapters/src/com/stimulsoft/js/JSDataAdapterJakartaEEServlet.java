/*
Stimulsoft.Reports.JS
Version: 2025.1.1
Build date: 2024.12.12
License: https://www.stimulsoft.com/en/licensing/reports
*/

package com.stimulsoft.js;

import java.io.IOException;

import com.stimulsoft.js.adapter.JSDataAdapter;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class JSDataAdapterJakartaEEServlet extends HttpServlet {

    private static final long serialVersionUID = 5187327772348131779L;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        process(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        process(req, resp);
    }

    private void process(HttpServletRequest req, HttpServletResponse resp) {
        try {
            String result = JSDataAdapter.process(req.getInputStream());
            resp.setHeader("Access-Control-Allow-Origin", "*");
            resp.setHeader("Cache-Control", "no-cache");
            resp.getOutputStream().write(result.getBytes("UTF-8"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
