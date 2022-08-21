package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
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

public class SearchActivity extends AppCompatActivity {

    private EditText searchValue;
    private ListView listView;
    private ArrayList<Search> detailsArrayList = new ArrayList<>();
    private ArrayList<Search> detailsArrayList2 = new ArrayList<>();

    String id = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);

        searchValue = findViewById(R.id.searchValue);
        listView = findViewById(R.id.listView);

        showDetails();

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                String selected = String.valueOf(detailsArrayList.get(i).getId());

                Intent intent = new Intent(SearchActivity.this, ServiceBranchDetailsActivity.class);
                intent.putExtra("id", selected);
                startActivity(intent);

            }
        });

        searchValue.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                searchDetails(charSequence.toString().toLowerCase());
            }

            @Override
            public void afterTextChanged(Editable editable) {

            }
        });

    }

    private void searchDetails(String value)
    {

        detailsArrayList.clear();
        listView.setAdapter(null);

        SearchAdapter searchAdapter = new SearchAdapter(this, R.layout.row_search_item, detailsArrayList);
        listView.setAdapter(searchAdapter);

        if (!value.equals("")) {
            for (int i = 0; i < detailsArrayList2.size(); i++) {
                if (detailsArrayList2.get(i).getDepartment().toLowerCase().contains(value) || detailsArrayList2.get(i).getBranch().toLowerCase().contains(value)) {
                    detailsArrayList.add(detailsArrayList2.get(i));
                }
            }
        } else {
            for (int i = 0; i < detailsArrayList2.size(); i++) {
                detailsArrayList.add(detailsArrayList2.get(i));
            }
        }

        searchAdapter.notifyDataSetChanged();

    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        SearchAdapter searchAdapter = new SearchAdapter(this, R.layout.row_search_item, detailsArrayList);
        listView.setAdapter(searchAdapter);

        String URL = API.BRANCHES_API + "/all";

        RequestQueue requestQueue = Volley.newRequestQueue(SearchActivity.this);
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
                                String department = (String) responseData.get(2);
                                String branch = (String) responseData.get(3);
                                String logo = API.ASSERT_URL + "/" +  ((String) responseData.get(10));

                                detailsArrayList.add(new Search(id, department, branch, logo));
                                detailsArrayList2.add(new Search(id, department, branch, logo));

                            }

                            searchAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(SearchActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}

class Search {

    String id, department, branch, logo;

    public Search(String id, String department, String branch, String logo) {
        this.id = id;
        this.department = department;
        this.branch = branch;
        this.logo = logo;
    }

    public String getId() {
        return id;
    }

    public String getDepartment() {
        return department;
    }

    public String getBranch() {
        return branch;
    }

    public String getLogo() {
        return logo;
    }
}

class SearchAdapter extends ArrayAdapter<Search> {

    private Context mContext;
    private int mResource;

    public SearchAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Search> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView departmentText = (TextView) convertView.findViewById(R.id.department);
        TextView branch = (TextView) convertView.findViewById(R.id.branch);
        ImageView logo = (ImageView) convertView.findViewById(R.id.logo);

        departmentText.setText(getItem(position).getDepartment());
        branch.setText(getItem(position).getBranch());

        Uri imgUri = Uri.parse(getItem(position).getLogo());
        Picasso.get().load(imgUri).into(logo);

        return convertView;
    }

}