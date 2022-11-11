package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

public class ViewInquiryCommentsActivity extends AppCompatActivity {

    private ListView listView;
    private EditText comment;
    private Button btnAdd;
    private ArrayList<Comment> detailsArrayList = new ArrayList<>();

    String id = "", status = "";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_inquiry_comments);


        Intent project = getIntent();
        id = project.getStringExtra("id");
        status = project.getStringExtra("status");

        comment = (EditText) findViewById(R.id.comment);
        btnAdd = (Button) findViewById(R.id.btnAdd);
        listView = (ListView) findViewById(R.id.listView);

        if (status.equals("completed")) {
            comment.setVisibility(View.GONE);
            btnAdd.setVisibility(View.GONE);
        }

        showDetails();

        btnAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                String strComment = comment.getText().toString();
                if (strComment.equals("") || id.equals("")) {
                    Toast.makeText(ViewInquiryCommentsActivity.this, "Fields empty!", Toast.LENGTH_SHORT).show();

                } else {

                    try {
                        String URL = API.INQUIRIES_API + "/comment/add";

                        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryCommentsActivity.this);
                        JSONObject jsonBody = new JSONObject();
                        jsonBody.put("id", id);
                        jsonBody.put("comment", strComment);

                        final String requestBody = jsonBody.toString();

                        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {

                                try {
                                    JSONObject jsonObject = new JSONObject(response);

                                    String status = jsonObject.getString("status");
                                    String msg = jsonObject.getString("msg");

                                    if (status.equals("success")) {
                                        comment.setText("");
                                        showDetails();
                                    }

                                    Toast.makeText(ViewInquiryCommentsActivity.this, msg, Toast.LENGTH_SHORT).show();

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                            }
                        }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {

                                Toast.makeText(ViewInquiryCommentsActivity.this, "Some error occur" + error.toString(), Toast.LENGTH_SHORT).show();
                            }
                        }) {
                            @Override
                            public String getBodyContentType() {
                                return "application/json; charset=utf-8";
                            }

                            @Override
                            public byte[] getBody() throws AuthFailureError {
                                try {
                                    return requestBody == null ? null : requestBody.getBytes("utf-8");
                                } catch (UnsupportedEncodingException uee) {
                                    return null;
                                }
                            }

                        };

                        requestQueue.add(stringRequest);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                }

            }
        });
    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        CommentAdapter commentAdapter = new CommentAdapter(this, R.layout.row_inquiry_comment_item, detailsArrayList);
        listView.setAdapter(commentAdapter);

        String URL = API.INQUIRIES_API + "/" + id + "/comments";

        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryCommentsActivity.this);
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                URL,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        try {

                            for (int index = 0; index < response.length(); index++) {

                                JSONArray responseData = response.getJSONArray(index);

                                String id = ((Number) responseData.get(0)).toString();
                                String comment = (String) responseData.get(2);

                                detailsArrayList.add(new Comment(id, comment));

                            }

                            commentAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ViewInquiryCommentsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}


class Comment {

    String id, comment;

    public Comment(String id, String comment) {
        this.id = id;
        this.comment = comment;
    }

    public String getId() {
        return id;
    }

    public String getComment() {
        return comment;
    }
}

class CommentAdapter extends ArrayAdapter<Comment> {

    private Context mContext;
    private int mResource;

    public CommentAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Comment> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView comment = (TextView) convertView.findViewById(R.id.comment);

        comment.setText(getItem(position).getComment());

        return convertView;
    }

}