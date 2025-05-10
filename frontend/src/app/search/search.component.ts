import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    FormsModule,
    MatIconModule
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  urlToSearch: string = '';

  @ViewChild('eye', { static: true }) eyeRef!: ElementRef;

  constructor(private apiService: ApiService, private renderer: Renderer2){}

  analyseUrl() {
    this.apiService.analyseUrl(this.urlToSearch).subscribe((response) => {
      console.log(response);
    })
  }

  ngAfterViewInit(): void {
    this.renderer.listen('document', 'mousemove', (event: MouseEvent) => {
      const eyeEl = this.eyeRef.nativeElement;
      const socketEl = eyeEl.parentElement!;
      const socketRect = socketEl.getBoundingClientRect();
  
      const centerX = socketRect.left + socketRect.width / 2;
      const centerY = socketRect.top + socketRect.height / 2;
  
      const deltaX = event.clientX - centerX;
      const deltaY = event.clientY - centerY;
  
      const angle = Math.atan2(deltaY, deltaX);
      const radius = 20; 
  
      const x = Math.cos(angle) * radius * 2;
      const y = Math.sin(angle) * radius;
  
      this.renderer.setStyle(eyeEl, 'transform', `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`);
    });
  }

}
