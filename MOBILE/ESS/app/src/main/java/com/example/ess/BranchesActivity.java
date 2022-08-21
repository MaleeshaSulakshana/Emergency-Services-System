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

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;

public class BranchesActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayList<Branch> detailsArrayList = new ArrayList<>();

    String id = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_branches);

        Intent project = getIntent();
        id = project.getStringExtra("id");

        listView = findViewById(R.id.listView);

        showDetails();

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                String selected = String.valueOf(detailsArrayList.get(i).getId());

                Intent intent = new Intent(BranchesActivity.this, ServiceBranchDetailsActivity.class);
                intent.putExtra("id", selected);
                startActivity(intent);

            }
        });

    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        BranchAdapter branchAdapter = new BranchAdapter(this, R.layout.row_branches_item, detailsArrayList);
        listView.setAdapter(branchAdapter);

        String URL = API.BRANCHES_API + "/all/" + id;

        RequestQueue requestQueue = Volley.newRequestQueue(BranchesActivity.this);
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
                                String title = (String) responseData.get(3);

                                detailsArrayList.add(new Branch(id, title));

                            }

                            branchAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(BranchesActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}

class Branch {

    String id, title;

    public Branch(String id, String title) {
        this.id = id;
        this.title = title;
    }

    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }
}

class BranchAdapter extends ArrayAdapter<Branch> {

    private Context mContext;
    private int mResource;

    public BranchAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Branch> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView title = (TextView) convertView.findViewById(R.id.title);
        title.setText(getItem(position).getTitle());

        return convertView;
    }

}