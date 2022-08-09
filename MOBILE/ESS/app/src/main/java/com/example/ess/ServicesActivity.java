package com.example.ess;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.media.Image;
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

import java.util.ArrayList;

public class ServicesActivity extends AppCompatActivity {

    private ListView listView;
    private ArrayList<Service> detailsArrayList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_services);

        listView = findViewById(R.id.listView);

        showDetails();

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int i, long id) {

                String selected = String.valueOf(detailsArrayList.get(i).getId());

                Intent intent = new Intent(ServicesActivity.this, BranchesActivity.class);
                intent.putExtra("id", selected);
                startActivity(intent);

            }
        });

    }

    private void showDetails()
    {
        detailsArrayList.clear();
        listView.setAdapter(null);

        ServiceAdapter serviceAdapter = new ServiceAdapter(this, R.layout.row_services_item, detailsArrayList);
        listView.setAdapter(serviceAdapter);

        detailsArrayList.add(new Service("1", "Police", "R.drawable.sl_police"));
        serviceAdapter.notifyDataSetChanged();

    }

}

class Service {

    String id, title, logo;

    public Service(String id, String title, String logo) {
        this.id = id;
        this.title = title;
        this.logo = logo;
    }

    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getLogo() {
        return logo;
    }
}

class ServiceAdapter extends ArrayAdapter<Service> {

    private Context mContext;
    private int mResource;

    public ServiceAdapter(@NonNull Context context, int resource, @NonNull ArrayList<Service> objects) {
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
        ImageView logo = (ImageView) convertView.findViewById(R.id.logo);

        title.setText(getItem(position).getTitle());
//        logo.setImageURI(Uri.parse(getItem(position).getLogo()));

        return convertView;
    }

}