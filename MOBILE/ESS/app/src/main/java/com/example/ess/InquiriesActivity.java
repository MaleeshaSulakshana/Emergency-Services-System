package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.example.ess.Classes.API;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

public class InquiriesActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayList<Inquiry> detailsArrayList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_inquiries);

        listView = findViewById(R.id.listView);

        showDetails();

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                String selected = String.valueOf(detailsArrayList.get(i).getId());

                Intent intent = new Intent(InquiriesActivity.this, BranchesActivity.class);
                intent.putExtra("id", selected);
                startActivity(intent);

            }
        });

    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        InquiryAdapter inquiryAdapter = new InquiryAdapter(this, R.layout.row_services_item, detailsArrayList);
        listView.setAdapter(inquiryAdapter);

        String URL = API.DEPARTMENT_API;

        RequestQueue requestQueue = Volley.newRequestQueue(InquiriesActivity.this);
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

                                String id = (String) responseData.get(1);
                                String desc = (String) responseData.get(2);
                                String date = (String) responseData.get(10);
                                int autoId = (int) responseData.get(0);

                                detailsArrayList.add(new Inquiry(id, desc, date, autoId));

                            }

                            inquiryAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(InquiriesActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}

class Inquiry {

    String id, desc, date;
    int autoId;

    public Inquiry(String id, String desc, String date, int autoId) {
        this.id = id;
        this.desc = desc;
        this.date = date;
        this.autoId = autoId;
    }

    public String getId() {
        return id;
    }

    public String getDesc() {
        return desc;
    }

    public String getDate() {
        return date;
    }

    public int getAutoId() {
        return autoId;
    }
}

class InquiryAdapter extends ArrayAdapter<Inquiry> {

    private Context mContext;
    private int mResource;

    public InquiryAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Inquiry> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

//        TextView title = (TextView) convertView.findViewById(R.id.title);
//        ImageView logo = (ImageView) convertView.findViewById(R.id.logo);
//
//        title.setText(getItem(position).getTitle());
//
//        Uri imgUri = Uri.parse(getItem(position).getLogo());
//        Picasso.get().load(imgUri).into(logo);

        return convertView;
    }

}