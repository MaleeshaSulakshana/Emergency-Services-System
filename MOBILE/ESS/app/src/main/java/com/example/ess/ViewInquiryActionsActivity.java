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

public class ViewInquiryActionsActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayList<Action> detailsArrayList = new ArrayList<>();

    String id = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_inquiry_actions);

        Intent project = getIntent();
        id = project.getStringExtra("id");

        listView = findViewById(R.id.listView);

        showDetails();
    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        ActionAdapter actionAdapter = new ActionAdapter(this, R.layout.row_inquiry_action_item, detailsArrayList);
        listView.setAdapter(actionAdapter);

        String URL = API.INQUIRIES_API + "/" + id + "/actions";

        RequestQueue requestQueue = Volley.newRequestQueue(ViewInquiryActionsActivity.this);
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
                                String action = (String) responseData.get(3);
                                String department = (String) responseData.get(4);
                                String branch = (String) responseData.get(5);
                                String branch_user = (String) responseData.get(6);
                                String date_time = (String) responseData.get(7);

                                detailsArrayList.add(new Action(id, action, department, branch, branch_user, date_time));

                            }

                            actionAdapter.notifyDataSetChanged();

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(ViewInquiryActionsActivity.this, error.toString(),Toast.LENGTH_SHORT).show();
                    }
                }

        );

        requestQueue.add(jsonArrayRequest);

    }

}


class Action {

    String id, actionDetails, department, branch, branchUser, date;

    public Action(String id, String actionDetails, String department, String branch, String branchUser, String date) {
        this.id = id;
        this.actionDetails = actionDetails;
        this.department = department;
        this.branch = branch;
        this.branchUser = branchUser;
        this.date = date;
    }

    public String getId() {
        return id;
    }

    public String getActionDetails() {
        return actionDetails;
    }

    public String getDepartment() {
        return department;
    }

    public String getBranch() {
        return branch;
    }

    public String getBranchUser() {
        return branchUser;
    }

    public String getDate() {
        return date;
    }
}

class ActionAdapter extends ArrayAdapter<Action> {

    private Context mContext;
    private int mResource;

    public ActionAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Action> objects) {
        super(context, resource, objects);

        this.mContext = context;
        this.mResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater layoutInflater = LayoutInflater.from(mContext);
        convertView = layoutInflater.inflate(mResource, parent, false);

        TextView actionDetails = (TextView) convertView.findViewById(R.id.actionDetails);
        TextView department = (TextView) convertView.findViewById(R.id.department);
        TextView branch = (TextView) convertView.findViewById(R.id.branch);
        TextView bUser = (TextView) convertView.findViewById(R.id.bUser);
        TextView date = (TextView) convertView.findViewById(R.id.date);

        actionDetails.setText(getItem(position).getActionDetails());
        department.setText(getItem(position).getDepartment());
        branch.setText(getItem(position).getBranch());
        bUser.setText(getItem(position).getBranchUser());
        date.setText(getItem(position).getDate());

        return convertView;
    }

}